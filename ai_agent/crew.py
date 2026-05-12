"""
TravelWatch AI - CrewAI Agent Workflow

Uses existing project structure:

TRAVELWATCHAI/
├── ai_agent/
│   └── crew.py
├── datasets/
│   └── Clean_Dataset.csv
└── streamlit_app/
    ├── model_weights/
    │   └── travelwatch_models.json
    ├── airports_db.py
    ├── prediction_engine.py
    └── skyscanner_api.py
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------------------

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
STREAMLIT_DIR = ROOT_DIR / "streamlit_app"

sys.path.append(str(STREAMLIT_DIR))

# ---------------------------------------------------------------------
# FORCE LOCAL OLLAMA
# ---------------------------------------------------------------------

os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_MODEL_NAME"] = "ollama/llama3.2:1b"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"

# ---------------------------------------------------------------------
# CREWAI IMPORTS
# ---------------------------------------------------------------------

from crewai import Agent, Crew, LLM, Process, Task

# ---------------------------------------------------------------------
# IMPORT EXISTING PROJECT FILES
# ---------------------------------------------------------------------

from airports_db import search_airports_local
from prediction_engine import predict_flight
from skyscanner_api import get_current_price, _api_key

# ---------------------------------------------------------------------
# LOCAL OLLAMA MODEL
# ---------------------------------------------------------------------

llm_local = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://localhost:11434",
    temperature=0.2,
)

# ---------------------------------------------------------------------
# DATA CLASS
# ---------------------------------------------------------------------

@dataclass
class WatchTask:
    origin: str = "UNKNOWN"
    destination: str = "UNKNOWN"
    departure_date: str = "UNKNOWN"
    target_price: Optional[float] = None
    currency: str = "USD"
    cabin_class: str = "Economy"
    adults: int = 1
    stops: int = 0

# ---------------------------------------------------------------------
# AIRPORT RESOLUTION
# ---------------------------------------------------------------------

def resolve_airport(raw: str) -> str:
    """
    Convert city names into airport/IATA codes using local airport DB.
    """

    if not raw:
        return "UNKNOWN"

    raw = raw.strip()

    if re.fullmatch(r"[A-Za-z]{3}", raw):
        return raw.upper()

    matches = search_airports_local(raw)

    if matches and len(matches) > 0:
        return matches[0]["skyId"]

    return raw.upper()

# ---------------------------------------------------------------------
# PARSE USER REQUEST
# ---------------------------------------------------------------------

def parse_watch_request(text: str) -> WatchTask:

    price_match = re.search(
        r"(?:under|below|budget|target)?\s*(?:\$|USD|INR|EUR|GBP)?\s*(\d{2,7})",
        text,
        flags=re.I,
    )

    target_price = float(price_match.group(1)) if price_match else None

    currency = "USD"

    if re.search(r"\bINR\b|₹", text, flags=re.I):
        currency = "INR"
    elif re.search(r"\bEUR\b|€", text, flags=re.I):
        currency = "EUR"
    elif re.search(r"\bGBP\b|£", text, flags=re.I):
        currency = "GBP"

    cabin_class = "Business" if re.search(r"business", text, flags=re.I) else "Economy"

    adults_match = re.search(
        r"(\d+)\s*(adult|adults|passenger|passengers)",
        text,
        flags=re.I,
    )

    adults = int(adults_match.group(1)) if adults_match else 1

    route = re.search(
        r"(?:from\s+)?([A-Za-z .]+?)\s+to\s+([A-Za-z .]+?)(?:\s+on|\s+under|\s+below|\s+budget|$)",
        text,
        flags=re.I,
    )

    origin_raw = route.group(1).strip() if route else "UNKNOWN"
    destination_raw = route.group(2).strip() if route else "UNKNOWN"

    origin = resolve_airport(origin_raw)
    destination = resolve_airport(destination_raw)

    date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)

    departure_date = date_match.group(1) if date_match else "UNKNOWN"

    return WatchTask(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        target_price=target_price,
        currency=currency,
        cabin_class=cabin_class,
        adults=adults,
        stops=0,
    )

# ---------------------------------------------------------------------
# BUILD FLIGHT DATA
# ---------------------------------------------------------------------

def build_flight_data(task: WatchTask) -> dict:

    target = int(task.target_price) if task.target_price else 500

    current_price = get_current_price(
        origin=task.origin,
        destination=task.destination,
        date=task.departure_date,
        target=target,
        cabin_class=task.cabin_class.lower(),
        adults=task.adults,
        currency=task.currency,
    )

    return {
        "origin": task.origin,
        "destination": task.destination,
        "dep_date": task.departure_date,
        "arr_date": task.departure_date,
        "current_price": current_price,
        "target": target,
        "currency": task.currency,
        "class": task.cabin_class,
        "stops": task.stops,
        "adults": task.adults,
    }

# ---------------------------------------------------------------------
# BOOKING LINK
# ---------------------------------------------------------------------

def booking_link(task: WatchTask) -> str:

    origin = task.origin.replace(" ", "+")
    destination = task.destination.replace(" ", "+")

    return (
        f"https://www.google.com/travel/flights?"
        f"q={origin}+to+{destination}+on+{task.departure_date}"
    )

# ---------------------------------------------------------------------
# FINAL OUTPUT
# ---------------------------------------------------------------------

def print_final_output(
    task: WatchTask,
    flight_data: dict,
    prediction: dict,
):

    recommendation = prediction.get("recommendation", "WAIT")

    confidence = prediction.get("confidence", 0)

    predicted_price = prediction.get(
        "predicted_price",
        flight_data["current_price"],
    )

    current_price = prediction.get(
        "current_price",
        flight_data["current_price"],
    )

    change_pct = prediction.get("change_pct", 0)

    change_dir = prediction.get("change_dir", "up")

    target = prediction.get(
        "target",
        flight_data["target"],
    )

    price_source = (
        "live Skyscanner/RapidAPI"
        if _api_key()
        else "estimated fallback"
    )

    print("\n")
    print("=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)

    print(f"\nFinal Recommendation: {recommendation}")

    if recommendation == "BUY":
        print(
            f"Reasoning: Current fare is below or near your target "
            f"and prices are expected to move {change_dir} "
            f"by approximately {change_pct}%."
        )
    else:
        print(
            f"Reasoning: Current fare is not attractive enough "
            f"relative to your target price."
        )

    print(f"\nCurrent Lowest Fare: {task.currency} {current_price}")

    print(f"Predicted Future Price: {task.currency} {predicted_price}")

    print(f"Target Price: {task.currency} {target}")

    print(f"Confidence: {confidence}%")

    print(f"Price Source: {price_source}")

    print(f"\nBooking/Search Link:")
    print(booking_link(task))

    print("\n" + "=" * 60)

# ---------------------------------------------------------------------
# CREWAI AGENTS
# ---------------------------------------------------------------------

watch_parser_agent = Agent(
    role="Watch Task Parser",
    goal="Convert natural language travel requests into structured watch tasks.",
    backstory=(
        "You extract route, date, target price, cabin class, "
        "currency, and passenger information."
    ),
    verbose=True,
    llm=llm_local,
)

fare_agent = Agent(
    role="Fare Aggregation Agent",
    goal="Explain the current flight pricing information.",
    backstory=(
        "You summarize retrieved flight fares and pricing conditions."
    ),
    verbose=True,
    llm=llm_local,
)

ml_agent = Agent(
    role="ML Analysis Agent",
    goal="Explain the ML-generated BUY/WAIT recommendation.",
    backstory=(
        "You explain TravelWatch AI price predictions, "
        "confidence scores, and trend estimates."
    ),
    verbose=True,
    llm=llm_local,
)



# ---------------------------------------------------------------------
# BUILD CREW
# ---------------------------------------------------------------------

def build_crew(
    user_request: str,
    task: WatchTask,
    flight_data: dict,
    prediction: dict,
):

    parse_task = Task(
        description=f"""
User Request:
{user_request}

Parsed Information:
- origin: {task.origin}
- destination: {task.destination}
- departure_date: {task.departure_date}
- target_price: {task.target_price}
- currency: {task.currency}
- cabin_class: {task.cabin_class}

Explain the structured watch task.
""",
        expected_output="Structured watch task explanation.",
        agent=watch_parser_agent,
    )

    fare_task = Task(
        description=f"""
Current Fare Data:
- current_price: {flight_data['current_price']}
- target: {flight_data['target']}
- currency: {task.currency}

Explain the fare situation.
""",
        expected_output="Fare analysis explanation.",
        agent=fare_agent,
        context=[parse_task],
    )

    analysis_task = Task(
        description=f"""
Prediction Output:
{prediction}

Explain:
- recommendation
- confidence
- predicted price
- expected trend
""",
        expected_output="ML recommendation explanation.",
        agent=ml_agent,
        context=[parse_task, fare_task],
    )

    return Crew(
        agents=[
            watch_parser_agent,
            fare_agent,
            ml_agent,
        ],
        tasks=[
            parse_task,
            fare_task,
            analysis_task,
        ],
        process=Process.sequential,
        verbose=True,
        tracing=False,
    )

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------

if __name__ == "__main__":

    user_watch_request = input(
        "\nEnter travel request:\n"
        "Example: DEL to BOM on 2026-05-20 under 5500 INR economy\n> "
    ).strip()

    task = parse_watch_request(user_watch_request)

    flight_data = build_flight_data(task)

    try:
        prediction = predict_flight(flight_data)

    except Exception as e:

        current_price = float(flight_data["current_price"])

        target = float(flight_data["target"])

        prediction = {
            "recommendation": (
                "BUY"
                if current_price <= target
                else "WAIT"
            ),
            "confidence": 60,
            "predicted_price": current_price,
            "current_price": current_price,
            "change_pct": 0,
            "change_dir": "unknown",
            "target": target,
            "error": str(e),
        }

    try:

        crew = build_crew(
            user_watch_request,
            task,
            flight_data,
            prediction,
        )

        crew.kickoff()

    except Exception as e:

        print("\nCrewAI explanation failed.")
        print(f"Reason: {e}")

    print_final_output(
        task,
        flight_data,
        prediction,
    )

