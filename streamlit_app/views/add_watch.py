import streamlit as st
from datetime import date, timedelta
from prediction_engine import predict_flight
from skyscanner_api import fetch_cheapest_price, _api_key, search_airports

CURRENCIES = ["USD", "INR", "EUR", "GBP", "JPY", "AED", "SGD", "HKD"]

# Fallback list when no API key is configured
_FALLBACK_CITIES = ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]
_CITY_TO_IATA = {
    "Bangalore": "BLR", "Chennai": "MAA", "Delhi": "DEL",
    "Hyderabad": "HYD", "Kolkata": "CCU", "Mumbai": "BOM",
}

CLASSES = ["Economy", "Business"]
STOPS_OPTIONS = [("Non-stop", 0), ("1 Stop", 1), ("2+ Stops", 2)]
TIMES = ["Early_Morning", "Morning", "Afternoon", "Evening", "Late_Night", "Night"]


def _airport_field(label: str, widget_key: str) -> dict | None:
    """
    Searchable airport picker powered by Skyscanner.
    Returns {"skyId": IATA, "entityId": ..., "name": display_name} or None.
    Falls back to a fixed Indian-city selectbox when no API key is set.
    """
    key = _api_key()

    if not key:
        city = st.selectbox(label, _FALLBACK_CITIES, label_visibility="collapsed", key=widget_key)
        iata = _CITY_TO_IATA.get(city, city)
        return {"skyId": iata, "entityId": "", "name": city}

    query = st.text_input(
        label,
        key=f"{widget_key}_q",
        placeholder="Type city or IATA code (e.g. London, Mumbai, JFK, SIN, DEL)...",
        label_visibility="collapsed",
    )

    if not query or len(query) < 2:
        st.caption("Type city, country, IATA code, or abbreviation (NY, LA, HK…)")
        return None

    results, _ = search_airports(query, key)
    if not results:
        st.caption("No airports found — try city name, country, or IATA code (e.g. London, India, JFK).")
        return None

    labels = [
        r["name"]
        + (f" — {r['subtitle']}" if r.get("subtitle") else "")
        + (f" ({r['skyId']})" if r.get("skyId") else "")
        for r in results
    ]
    idx = st.selectbox(
        "Airport",
        range(len(results)),
        format_func=lambda i: labels[i],
        key=f"{widget_key}_sel",
        label_visibility="collapsed",
    )
    return results[idx]


def render():
    # ── Header ────────────────────────────────────────────────────────────────
    col_title, col_btn = st.columns([5, 1])
    with col_title:
        back_col, title_col = st.columns([1, 10])
        with back_col:
            if st.button("←", key="back_btn"):
                st.session_state.page = "Dashboard"
                st.rerun()
        with title_col:
            st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0;">Add New Watch</h2>', unsafe_allow_html=True)
    with col_btn:
        start_btn = st.button("Start Watching", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Airport search fields ─────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Origin <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    origin_info = _airport_field("Origin", "origin")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Destination <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    dest_info = _airport_field("Destination", "dest")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Departure Date <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    dep_date = st.date_input("Departure Date", value=date.today() + timedelta(days=30),
                             min_value=date.today(), label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Arrival Date <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    arr_date = st.date_input("Arrival Date", value=date.today() + timedelta(days=37),
                             min_value=date.today(), label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Target Price <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    target_price = st.number_input("Target Price", min_value=10, max_value=500000,
                                   value=300, step=10, label_visibility="collapsed")

    col_cur, col_adt = st.columns(2)
    with col_cur:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-label">Currency <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
        currency = st.selectbox("Currency", options=CURRENCIES, index=0,
                                placeholder="Select Currency", label_visibility="collapsed")
    with col_adt:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-label">Adults <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
        adults = st.number_input("Adults", min_value=1, max_value=9, value=1, step=1,
                                 label_visibility="collapsed")

    # ── Optional flight details ───────────────────────────────────────────────
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown('<div style="color:#9ca3af; font-size:12px; margin-bottom:12px;">Flight Details (Optional — improves BUY/WAIT prediction)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-label">Class</div>', unsafe_allow_html=True)
        class_type = st.selectbox("Class", options=CLASSES, index=0, label_visibility="collapsed")
    with col2:
        st.markdown('<div class="sec-label">Number of Stops</div>', unsafe_allow_html=True)
        stops_label, stops_val = st.selectbox(
                "Stops",
                options=STOPS_OPTIONS,
                index=0,
                format_func=lambda x: x[0],
                label_visibility="collapsed",
        )

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="sec-label">Departure Time</div>', unsafe_allow_html=True)
        dep_time = st.selectbox("Departure Time", options=TIMES, index=4,
                                label_visibility="collapsed")
    with col4:
        st.markdown('<div class="sec-label">Arrival Time</div>', unsafe_allow_html=True)
        arr_time = st.selectbox("Arrival Time", options=TIMES, index=2,
                                label_visibility="collapsed")

    # ── Submit ────────────────────────────────────────────────────────────────
    if start_btn:
        if not origin_info:
            st.error("Please select an origin airport.")
        elif not dest_info:
            st.error("Please select a destination airport.")
        elif origin_info["skyId"] == dest_info["skyId"] and origin_info["skyId"]:
            st.error("Origin and destination cannot be the same.")
        elif dep_date >= arr_date:
            st.error("Arrival date must be after departure date.")
        else:
            try:
                origin_id = origin_info["skyId"]   # IATA code or city name
                dest_id = dest_info["skyId"]

                with st.spinner("Fetching live price from Skyscanner..."):
                    api_result = fetch_cheapest_price(
                        origin_id, dest_id, str(dep_date),
                        class_type.lower(), _api_key(),
                        adults=int(adults), currency=currency,
                        origin_entity_id=origin_info.get("entityId", ""),
                        destination_entity_id=dest_info.get("entityId", ""),
                    )

                api_price = api_result.get("price")
                api_currency = api_result.get("currency", currency)
                err = api_result.get("error", "")
                if api_price:
                    current_price = api_price
                    currency = api_currency
                    st.info(f"Live Skyscanner price: {currency} {current_price:,}")
                elif err == "no_key":
                    st.error("Skyscanner API key not configured. Add RAPIDAPI_KEY to create watches with live prices.")
                    return
                else:
                    current_price = target_price
                    hint = "rate limited (429)" if "429" in str(err) else err
                    st.warning(
                        f"Live price unavailable ({hint}) — watch created using your target price as a placeholder. "
                        "The price will update next time you refresh."
                    )

                flight_data = {
                    "origin": origin_id,
                    "destination": dest_id,
                    "dep_date": str(dep_date),
                    "arr_date": str(arr_date),
                    "current_price": current_price,
                    "target": target_price,
                    "class": class_type,
                    "stops": stops_val,
                    "departure_time": dep_time,
                    "arrival_time": arr_time,
                }

                prediction = predict_flight(flight_data)

                new_id = (max((w["id"] for w in st.session_state.watches), default=0)) + 1
                price_source = "live" if api_result.get("price") else "estimated"
                new_watch = {
                    "id": new_id,
                    "origin": origin_id,
                    "origin_entity_id": origin_info.get("entityId", ""),
                    "dest": dest_id,
                    "dest_entity_id": dest_info.get("entityId", ""),
                    "dep_date": str(dep_date),
                    "arr_date": str(arr_date),
                    "target": target_price,
                    "currency": currency,
                    "adults": int(adults),
                    "class": class_type,
                    "stops": stops_val,
                    "current_price": current_price,
                    "recommendation": prediction["recommendation"],
                    "confidence": prediction["confidence"],
                    "change_pct": prediction["change_pct"],
                    "change_dir": prediction["change_dir"],
                    "predicted_price": prediction["predicted_price"],
                    "price_source": price_source,
                    "price_history": [
                        {
                            "date": str(date.today()),
                            "price": current_price,
                            "source": price_source,
                        }
                    ],
                }
                st.session_state.watches.insert(0, new_watch)
                st.session_state.selected_watch_id = new_id

                st.session_state.page = "Task Detail"
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")
                _cp = locals().get("current_price", target_price)
                rec = "BUY" if _cp <= target_price * 1.05 else "WAIT"
                st.warning(f"Fallback recommendation: {rec}")
