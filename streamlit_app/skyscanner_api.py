"""
Skyscanner live flight prices via RapidAPI Sky Scrapper.

Configure by setting RAPIDAPI_KEY in the environment or .streamlit/secrets.toml:
    RAPIDAPI_KEY = "your-key-here"
"""

import os
import tomllib
from functools import lru_cache
from pathlib import Path

import requests
import streamlit as st
from airports_db import search_airports_local

_BASE = "https://sky-scrapper.p.rapidapi.com"
_HOST = "sky-scrapper.p.rapidapi.com"

# Map currency -> (market locale, country code) used by Skyscanner's API.
# Falls back to ("en-US", "US") for anything not listed.
_CURRENCY_MARKET = {
    "USD": ("en-US", "US"),
    "EUR": ("en-GB", "GB"),
    "GBP": ("en-GB", "GB"),
    "INR": ("en-IN", "IN"),
    "JPY": ("ja-JP", "JP"),
    "AED": ("en-AE", "AE"),
    "SGD": ("en-SG", "SG"),
    "HKD": ("en-HK", "HK"),
    "AUD": ("en-AU", "AU"),
    "CAD": ("en-CA", "CA"),
    "CNY": ("zh-CN", "CN"),
    "KRW": ("ko-KR", "KR"),
    "CHF": ("de-CH", "CH"),
}

_FALLBACK_AIRPORTS = [
    {"skyId": "ATL", "entityId": "", "name": "Atlanta Hartsfield-Jackson", "subtitle": "Atlanta, United States"},
    {"skyId": "BOM", "entityId": "", "name": "Mumbai", "subtitle": "Mumbai, India"},
    {"skyId": "BLR", "entityId": "", "name": "Bengaluru", "subtitle": "Bangalore, India"},
    {"skyId": "CDG", "entityId": "", "name": "Paris Charles de Gaulle", "subtitle": "Paris, France"},
    {"skyId": "CCU", "entityId": "", "name": "Kolkata", "subtitle": "Kolkata, India"},
    {"skyId": "DEL", "entityId": "", "name": "Indira Gandhi International", "subtitle": "Delhi, India"},
    {"skyId": "DFW", "entityId": "", "name": "Dallas Fort Worth International", "subtitle": "Dallas, United States"},
    {"skyId": "DXB", "entityId": "", "name": "Dubai", "subtitle": "Dubai, United Arab Emirates"},
    {"skyId": "EWR", "entityId": "", "name": "Newark Liberty International", "subtitle": "New York, United States"},
    {"skyId": "HKG", "entityId": "", "name": "Hong Kong International", "subtitle": "Hong Kong"},
    {"skyId": "HYD", "entityId": "", "name": "Hyderabad", "subtitle": "Hyderabad, India"},
    {"skyId": "JFK", "entityId": "", "name": "New York John F. Kennedy", "subtitle": "New York, United States"},
    {"skyId": "LAX", "entityId": "", "name": "Los Angeles International", "subtitle": "Los Angeles, United States"},
    {"skyId": "LHR", "entityId": "", "name": "London Heathrow", "subtitle": "London, United Kingdom"},
    {"skyId": "MAA", "entityId": "", "name": "Chennai", "subtitle": "Chennai, India"},
    {"skyId": "ORD", "entityId": "", "name": "Chicago O'Hare International", "subtitle": "Chicago, United States"},
    {"skyId": "SFO", "entityId": "", "name": "San Francisco International", "subtitle": "San Francisco, United States"},
    {"skyId": "SIN", "entityId": "", "name": "Singapore Changi", "subtitle": "Singapore"},
    {"skyId": "SYD", "entityId": "", "name": "Sydney", "subtitle": "Sydney, Australia"},
    {"skyId": "NRT", "entityId": "", "name": "Tokyo Narita", "subtitle": "Tokyo, Japan"},
]


def _market_for(currency: str) -> tuple[str, str]:
    return _CURRENCY_MARKET.get((currency or "USD").upper(), ("en-US", "US"))


def _api_key() -> str:
    key = os.environ.get("RAPIDAPI_KEY", "")
    if not key:
        key = _secret("RAPIDAPI_KEY", "")
    return key


def _headers(key: str) -> dict:
    return {"x-rapidapi-key": key, "x-rapidapi-host": _HOST}


def _airport_ids(place: dict) -> tuple[str, str]:
    params = (
        place.get("navigation", {}).get("relevantFlightParams", {})
        or place.get("relevantFlightParams", {})
        or {}
    )
    sky_id = place.get("skyId") or params.get("skyId") or params.get("flightPlaceId") or ""
    entity_id = place.get("entityId") or params.get("entityId") or ""
    return sky_id, entity_id


def _airport_name(place: dict, fallback: str) -> tuple[str, str]:
    pres = place.get("presentation", {}) or {}
    nav = place.get("navigation", {}) or {}
    name = pres.get("title") or nav.get("localizedName") or place.get("name") or fallback
    subtitle = pres.get("subtitle") or place.get("subtitle") or ""
    return name, subtitle


def _fallback_airport_search(query: str, limit: int = 8) -> list[dict]:
    q = (query or "").strip().lower()
    if len(q) < 2:
        return []
    matches = []
    for airport in _FALLBACK_AIRPORTS:
        haystack = " ".join(
            [airport["skyId"], airport["name"], airport.get("subtitle", "")]
        ).lower()
        if q in haystack:
            matches.append(airport)
    return matches[:limit]


def _secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, "")
        if value:
            return value
    except Exception:
        pass
    return _local_secrets().get(name, default)


@lru_cache(maxsize=1)
def _local_secrets() -> dict:
    for path in (
        Path(__file__).resolve().parent / ".streamlit" / "secrets.toml",
    ):
        if path.exists():
            try:
                with path.open("rb") as fh:
                    return tomllib.load(fh)
            except Exception:
                return {}
    return {}


@st.cache_data(ttl=86400, show_spinner=False)
def _airport_entity(city: str, api_key: str) -> dict | None:
    """Resolve city name → {skyId, entityId}. Cached 24 h."""
    if not api_key:
        return None
    try:
        r = requests.get(
            f"{_BASE}/api/v1/flights/searchAirport",
            headers=_headers(api_key),
            params={"query": city, "locale": "en-US"},
            timeout=10,
        )
        r.raise_for_status()
        places = r.json().get("data", [])
        # Prefer AIRPORT entity over CITY
        for p in places:
            if p.get("navigation", {}).get("entityType") == "AIRPORT":
                sky_id, entity_id = _airport_ids(p)
                if sky_id:
                    return {"skyId": sky_id, "entityId": entity_id}
        if places:
            p = places[0]
            sky_id, entity_id = _airport_ids(p)
            if sky_id:
                return {"skyId": sky_id, "entityId": entity_id}
    except Exception:
        pass
    for airport in _fallback_airport_search(city, limit=1):
        return {"skyId": airport["skyId"], "entityId": airport["entityId"]}
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_cheapest_price(
    origin: str,
    destination: str,
    date: str,
    cabin_class: str,
    api_key: str,
    adults: int = 1,
    currency: str = "USD",
    origin_entity_id: str = "",
    destination_entity_id: str = "",
) -> dict:
    """
    Return {"price": int, "currency": currency} or {"price": None, "error": reason}.
    Results cached for 1 hour.
    """
    if not api_key:
        return {"price": None, "error": "no_key"}

    o = {"skyId": origin, "entityId": origin_entity_id} if origin_entity_id else _airport_entity(origin, api_key)
    d = {"skyId": destination, "entityId": destination_entity_id} if destination_entity_id else _airport_entity(destination, api_key)
    if not o or not d:
        return {"price": None, "error": "airport_not_found"}

    market, country = _market_for(currency)
    try:
        r = requests.get(
            f"{_BASE}/api/v1/flights/searchFlights",
            headers=_headers(api_key),
            params={
                "originSkyId": o["skyId"],
                "destinationSkyId": d["skyId"],
                "originEntityId": o["entityId"],
                "destinationEntityId": d["entityId"],
                "date": date,
                "cabinClass": cabin_class,
                "adults": str(max(1, int(adults))),
                "sortBy": "best",
                "currency": (currency or "USD").upper(),
                "market": market,
                "countryCode": country,
            },
            timeout=15,
        )
        r.raise_for_status()
        itineraries = r.json().get("data", {}).get("itineraries", [])
        prices = [
            it["price"]["raw"]
            for it in itineraries
            if it.get("price", {}).get("raw")
        ]
        if prices:
            return {"price": int(min(prices)), "currency": (currency or "USD").upper()}
        return {"price": None, "error": "no_flights"}
    except requests.Timeout:
        return {"price": None, "error": "timeout"}
    except Exception as e:
        return {"price": None, "error": str(e)}


def search_airports(query: str, api_key: str) -> tuple[list[dict], str | None]:
    """
    Return (results, error_message).
    Always searches the bundled local database first (instant, zero quota).
    Returns (local_results, None) — no API calls for airport search.
    """
    if len(query) < 2:
        return [], None
    return search_airports_local(query), None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_top_itineraries(
    origin: str,
    destination: str,
    date: str,
    cabin_class: str,
    adults: int,
    api_key: str,
    limit: int = 5,
    currency: str = "USD",
    origin_entity_id: str = "",
    destination_entity_id: str = "",
) -> list[dict]:
    """
    Return the top `limit` cheapest itineraries for the route, each as:
        {price, currency, carrier, stops, duration_min, depart, arrive}
    Empty list if the API key is missing or the request fails.
    """
    if not api_key:
        return []

    o = {"skyId": origin, "entityId": origin_entity_id} if origin_entity_id else _airport_entity(origin, api_key)
    d = {"skyId": destination, "entityId": destination_entity_id} if destination_entity_id else _airport_entity(destination, api_key)
    if not o or not d:
        return []

    cur = (currency or "USD").upper()
    market, country = _market_for(cur)
    try:
        r = requests.get(
            f"{_BASE}/api/v1/flights/searchFlights",
            headers=_headers(api_key),
            params={
                "originSkyId": o["skyId"],
                "destinationSkyId": d["skyId"],
                "originEntityId": o["entityId"],
                "destinationEntityId": d["entityId"],
                "date": date,
                "cabinClass": cabin_class,
                "adults": str(max(1, int(adults))),
                "sortBy": "best",
                "currency": cur,
                "market": market,
                "countryCode": country,
            },
            timeout=15,
        )
        r.raise_for_status()
        itineraries = r.json().get("data", {}).get("itineraries", []) or []
        out: list[dict] = []
        for it in itineraries[:limit]:
            price = (it.get("price") or {}).get("raw")
            if not price:
                continue
            legs = it.get("legs") or []
            leg = legs[0] if legs else {}
            carriers = ((leg.get("carriers") or {}).get("marketing") or [])
            carrier_name = carriers[0].get("name") if carriers else "—"
            out.append({
                "price": int(price),
                "currency": cur,
                "carrier": carrier_name,
                "stops": int(leg.get("stopCount", 0) or 0),
                "duration_min": int(leg.get("durationInMinutes", 0) or 0),
                "depart": leg.get("departure", ""),
                "arrive": leg.get("arrival", ""),
            })
        return out
    except Exception:
        return []


def skyscanner_search_url(origin: str, destination: str, dep_date: str,
                          cabin_class: str = "economy", adults: int = 1) -> str:
    """
    Build a public Skyscanner search URL for the given route/date.
    Format: https://www.skyscanner.com/transport/flights/<orig>/<dest>/<yymmdd>/?...
    Falls back to the homepage search if the date can't be parsed.
    """
    try:
        from datetime import datetime
        d = datetime.strptime(str(dep_date), "%Y-%m-%d").date()
        ymd = d.strftime("%y%m%d")
    except Exception:
        return "https://www.skyscanner.com/"

    o = (origin or "").lower()
    dst = (destination or "").lower()
    qs = f"?adultsv2={max(1, int(adults))}&cabinclass={cabin_class.lower()}&rtn=0"
    return f"https://www.skyscanner.com/transport/flights/{o}/{dst}/{ymd}/{qs}"

def get_current_price(
    origin: str,
    destination: str,
    date: str,
    target: int,
    cabin_class: str = "economy",
    adults: int = 1,
    currency: str = "USD",
) -> int:
    """
    Return live Skyscanner price if available.
    If unavailable, return estimated fallback around target price.
    """
    result = fetch_cheapest_price(
        origin=origin,
        destination=destination,
        date=date,
        cabin_class=cabin_class,
        api_key=_api_key(),
        adults=adults,
        currency=currency,
    )

    if result.get("price"):
        return int(result["price"])

    # fallback estimate if no API key / no flights / API error
    return int(target)