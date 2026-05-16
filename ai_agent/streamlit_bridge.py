from __future__ import annotations

import sys
from pathlib import Path

from datetime import date
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
STREAMLIT_DIR = ROOT_DIR / "streamlit_app"

sys.path.append(str(STREAMLIT_DIR))

from ai_agent.crew import (
    booking_link,
    build_crew,
    build_flight_data,
    parse_watch_request,
)

from prediction_engine import predict_flight


def _build_local_explanation(task, flight_data: dict[str, Any], prediction: dict[str, Any]) -> str:
    recommendation = prediction.get("recommendation", "WAIT")
    confidence = prediction.get("confidence", 0)
    current_price = prediction.get("current_price", flight_data.get("current_price"))
    predicted_price = prediction.get("predicted_price", current_price)
    target = flight_data.get("target")
    change_pct = prediction.get("change_pct", 0)
    change_dir = prediction.get("change_dir", "unknown")

    if recommendation == "BUY":
        reason = (
            "The current fare is at or near the target price, so this looks like a good time to book."
        )
    else:
        reason = (
            "The current fare is not attractive enough against the target price, so waiting is safer."
        )

    return (
        f"{recommendation} recommendation for {task.origin} to {task.destination} "
        f"on {task.departure_date}. {reason} Current fare is {task.currency} {current_price}, "
        f"predicted price is {task.currency} {predicted_price}, target is {task.currency} {target}, "
        f"and the model expects prices to move {change_dir} by about {change_pct}%. "
        f"Confidence: {confidence}%."
    )


def run_agent_request(user_request: str, use_crew_explanation: bool = False) -> dict[str, Any]:
    task = parse_watch_request(user_request)
    flight_data = build_flight_data(task)

    try:
        prediction = predict_flight(flight_data)
    except Exception as exc:
        current_price = float(flight_data.get("current_price") or flight_data.get("target") or 0)
        target = float(flight_data.get("target") or current_price)

        prediction = {
            "recommendation": "BUY" if current_price <= target else "WAIT",
            "confidence": 60,
            "predicted_price": current_price,
            "current_price": current_price,
            "change_pct": 0,
            "change_dir": "unknown",
            "target": target,
            "error": str(exc),
        }

    explanation = _build_local_explanation(task, flight_data, prediction)
    crew_error = ""

    if use_crew_explanation:
        try:
            crew = build_crew(user_request, task, flight_data, prediction)
            crew_result = crew.kickoff()
            explanation = str(crew_result)
        except Exception as exc:
            crew_error = str(exc)

    current_price = prediction.get("current_price", flight_data.get("current_price"))
    predicted_price = prediction.get("predicted_price", current_price)

    return {
        "origin": task.origin,
        "destination": task.destination,
        "departure_date": task.departure_date,
        "arrival_date": task.departure_date,
        "target": flight_data.get("target"),
        "currency": task.currency,
        "cabin_class": task.cabin_class,
        "adults": task.adults,
        "stops": task.stops,
        "current_price": current_price,
        "predicted_price": predicted_price,
        "recommendation": prediction.get("recommendation", "WAIT"),
        "confidence": prediction.get("confidence", 0),
        "change_pct": prediction.get("change_pct", 0),
        "change_dir": prediction.get("change_dir", "unknown"),
        "booking_link": booking_link(task),
        "price_source": "live_or_fallback",
        "explanation": explanation,
        "crew_error": crew_error,
        "raw_prediction": prediction,
        "raw_flight_data": flight_data,
        "created_date": str(date.today()),
    }
