from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from ai_agent.streamlit_bridge import run_agent_request


def _add_agent_result_to_watches(result: dict) -> None:
    new_id = max((watch["id"] for watch in st.session_state.watches), default=0) + 1

    new_watch = {
        "id": new_id,
        "origin": result["origin"],
        "dest": result["destination"],
        "dep_date": result["departure_date"],
        "arr_date": result["arrival_date"],
        "target": result["target"],
        "currency": result["currency"],
        "adults": result["adults"],
        "class": result["cabin_class"],
        "stops": result["stops"],
        "current_price": result["current_price"],
        "recommendation": result["recommendation"],
        "confidence": result["confidence"],
        "change_pct": result["change_pct"],
        "change_dir": result["change_dir"],
        "predicted_price": result["predicted_price"],
        "price_source": result["price_source"],
        "booking_link": result["booking_link"],
        "price_history": [
            {
                "date": result["created_date"],
                "price": result["current_price"],
                "source": result["price_source"],
            }
        ],
    }

    st.session_state.watches.insert(0, new_watch)
    st.session_state.selected_watch_id = new_id


def render():
    st.markdown(
        '<h2 style="font-size:24px;font-weight:700;color:#111;margin:0;">AI Agent</h2>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    user_request = st.text_area(
        "Travel request",
        placeholder="Example: DEL to BOM on 2026-05-20 under 5500 INR economy",
        height=110,
        label_visibility="collapsed",
    )

    use_crew = st.checkbox("Use CrewAI explanation", value=False)

    run_btn = st.button("Run Agent", type="primary")

    if run_btn:
        if not user_request.strip():
            st.error("Enter a travel request first.")
            return

        with st.spinner("Running TravelWatch AI agent..."):
            result = run_agent_request(user_request.strip(), use_crew_explanation=use_crew)

        st.session_state.agent_result = result

    result = st.session_state.get("agent_result")

    if not result:
        return

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Route", f"{result['origin']} -> {result['destination']}")
    col2.metric("Current Price", f"{result['currency']} {result['current_price']}")
    col3.metric("Predicted Price", f"{result['currency']} {result['predicted_price']}")
    col4.metric("Recommendation", result["recommendation"])

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="tw-card">
            <div style="font-size:13px;color:#6b7280;margin-bottom:8px;">Agent Result</div>
            <div style="font-size:18px;font-weight:700;color:#111;">
                {result["recommendation"]} with {result["confidence"]}% confidence
            </div>
            <div style="font-size:14px;color:#4b5563;margin-top:8px;">
                Expected price movement: {result["change_dir"]} by {result["change_pct"]}%.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result.get("explanation"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.write(result["explanation"])

    st.markdown("<br>", unsafe_allow_html=True)

    col_add, col_link = st.columns([1, 1])

    with col_add:
        if st.button("Add To Watch List", type="primary", use_container_width=True):
            _add_agent_result_to_watches(result)
            st.success("Added to watch list.")
            st.session_state.page = "Dashboard"
            st.rerun()

    with col_link:
        st.link_button("Open Booking Search", result["booking_link"], use_container_width=True)
