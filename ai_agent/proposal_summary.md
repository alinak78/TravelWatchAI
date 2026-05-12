# Proposal Summary: TravelWatch AI Agent System

TravelWatch AI addresses the problem of volatile flight and train prices. Travelers often do not know whether to buy now or wait, and existing tools usually stop at passive alerts. This project turns the original travel-planning multi-agent system into a price-monitoring and decision-making system.

The CrewAI workflow has four agents. The Price Scout Agent converts the user's raw request into a structured watch task. The ML Analyst Agent simulates the proposed machine-learning pipeline using regression-style price prediction, classification-style Buy/Wait reasoning, and anomaly detection. The Risk and Constraint Reviewer Agent checks whether the recommendation is safe, budget-aware, and consistent with the user's constraints. The Booking and Notification Agent produces the final user-facing recommendation and includes a human approval step before any booking action.

This matches the proposal because the system moves from prediction to action. Instead of only saying what the price might be, it recommends BUY, WAIT, WATCH, or ALERT and explains the next step. In a deployed version, the same workflow could be connected to a Streamlit interface, FastAPI backend, Amadeus or other travel APIs, exchange-rate APIs, and saved ML models trained on historical fare datasets.
