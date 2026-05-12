# TravelWatch AI – Multi-Agent Travel Price Intelligence System

## Overview

TravelWatch AI is a multi-agent machine learning system for travel price monitoring, Buy/Wait prediction, and recommendation support. Instead of focusing on itinerary generation, the project treats travel booking as a **price intelligence and decision-making problem**.

The system combines:
- real-time fare retrieval,
- machine learning price prediction,
- Buy/Wait classification,
- anomaly detection,
- and agent-based reasoning

into a unified workflow that helps users decide when to purchase travel tickets.

The project integrates:
- CrewAI agents,
- local Ollama-hosted LLMs,
- live Skyscanner/RapidAPI pricing,
- and pre-trained ML models.

---

# Key Features

- Multi-agent CrewAI workflow
- Local Ollama LLM integration (no OpenAI API required)
- Real-time or fallback flight pricing
- Buy/Wait recommendation engine
- Ridge Regression price forecasting
- Logistic Regression classification
- Airport resolution using local airport database
- Human-in-the-loop booking workflow
- Deterministic final recommendation output

---

# System Architecture

The workflow consists of four stages:

## 1. Watch Task Parser

Converts natural-language travel requests into structured monitoring tasks.

### Example Input

```text
DEL to BOM on 2026-05-20 under 5500 INR economy
```

### Extracted Fields

- origin
- destination
- departure date
- target price
- currency
- cabin class
- passenger count

---

## 2. Real-Time Fare Aggregation

Retrieves:
- live Skyscanner prices through RapidAPI,
- or deterministic fallback pricing if API keys are unavailable.

The system:
- normalizes prices,
- identifies the current lowest fare,
- compares fares against user targets.

---

## 3. ML Analysis

The ML pipeline predicts:
- future price behavior,
- BUY/WAIT recommendation,
- confidence score,
- expected price movement.

### Models Used

#### Regression
- Ridge Regression
- Lasso Regression
- Polynomial Regression

#### Classification
- Logistic Regression
- KNN Classification

#### Anomaly Detection
- Z-score filtering
- IQR-based detection

---

## 4. Decision & Execution Layer

The final stage outputs:
- BUY or WAIT recommendation,
- confidence estimate,
- current lowest fare,
- predicted future fare,
- booking/search link.

Importantly:
- the system does not automatically purchase tickets,
- the user remains fully in control.

---

# Project Structure

```text
TRAVELWATCHAI/
│
├── ai_agent/
│   ├── crew.py
│   ├── README.md
│   ├── proposal_summary.md
│   ├── requirements.txt
│   └── .venv/
│
├── datasets/
│   └── Clean_Dataset.csv
│
├── notebooks/
│   └── travelwatchai.ipynb
│
├── streamlit_app/
│   ├── model_weights/
│   │   └── travelwatch_models.json
│   │
│   ├── views/
│   │
│   ├── airports_db.py
│   ├── app.py
│   ├── prediction_engine.py
│   └── skyscanner_api.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Core Components

## `crew.py`

Main CrewAI orchestration workflow.

Responsibilities:
- parsing travel requests,
- calling pricing functions,
- invoking prediction models,
- generating final recommendations,
- coordinating agents.

---

## `prediction_engine.py`

Contains the ML inference pipeline.

### Key Functionality
- Ridge Regression price prediction
- Logistic Regression BUY/WAIT classification
- feature engineering
- standardized inputs
- anomaly detection
- confidence estimation

---

## `skyscanner_api.py`

Handles:
- live flight pricing retrieval,
- RapidAPI integration,
- airport resolution,
- fallback pricing generation.

If no API key is provided, the system automatically generates deterministic estimated prices.

---

## `airports_db.py`

Local airport database for:
- IATA code resolution,
- airport search,
- city-to-airport matching.

This avoids unnecessary API requests.

---

# Technologies Used

## Core Frameworks
- CrewAI
- Ollama
- LiteLLM
- Streamlit

## Languages
- Python 3.11+

## ML Libraries
- NumPy
- scikit-learn
- pandas

## APIs
- Skyscanner RapidAPI

---

# Installation Guide

## 1. Install Python 3.11+

Verify:

```bash
python3.11 --version
```

---

## 2. Create Virtual Environment

```bash
python3.11 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install crewai ollama litellm streamlit numpy pandas requests scikit-learn
```

Or:

```bash
pip install -r requirements.txt
```

---

# Installing Ollama

## Mac

```bash
brew install --cask ollama
```

Open Ollama:

```bash
open -a Ollama
```

Verify:

```bash
ollama --version
```

---

# Download Local LLM

```bash
ollama pull llama3.2:1b
```

---

# Running the Project

## Start Ollama

Open terminal #1:

```bash
ollama serve
```

Keep this terminal running.

---

## Run CrewAI Workflow

Open terminal #2:

```bash
cd ai_agent

source .venv/bin/activate

python crew.py
```

---

# Example Input

```text
DEL to BOM on 2026-05-20 under 5500 INR economy
```

---

# Example Final Output

```text
============================================================

FINAL OUTPUT

============================================================

Final Recommendation: BUY

Reasoning:
Current fare is below or near your target and prices are expected
to increase closer to departure.

Current Lowest Fare: INR 5120

Predicted Future Price: INR 5480

Target Price: INR 5500

Confidence: 82%

Price Source: live Skyscanner/RapidAPI

Booking/Search Link:
https://www.google.com/travel/flights?q=DEL+to+BOM

============================================================
```

---

# CrewAI Workflow

The system uses three primary CrewAI agents:

## Watch Task Parser Agent
Extracts:
- origin,
- destination,
- date,
- target price,
- currency,
- cabin class.

---

## Fare Aggregation Agent
Explains:
- retrieved pricing,
- price source,
- target comparison,
- route conditions.

---

## ML Analysis Agent
Explains:
- BUY/WAIT recommendation,
- confidence score,
- predicted trend,
- model reasoning.

---

# Why Multi-Agent Architecture?

The travel pricing problem naturally decomposes into:
- parsing,
- retrieval,
- prediction,
- recommendation,
- execution support.

Separating these tasks into specialized agents:
- improves modularity,
- improves interpretability,
- reduces agent complexity,
- and enables reusable workflows.

---

# Common Errors & Fixes

## Error: `ModuleNotFoundError: No module named 'streamlit'`

Install dependencies:

```bash
pip install streamlit
```

---

## Error: `ModuleNotFoundError: No module named 'crewai'`

Install CrewAI:

```bash
pip install crewai litellm
```

---

## Error: `zsh: command not found: ollama`

Install Ollama:

```bash
brew install --cask ollama
```

---

## Error: `Failed to connect to OpenAI API`

Cause:
CrewAI falling back to OpenAI.

Fix:
Ensure `crew.py` contains:

```python
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_MODEL_NAME"] = "ollama/llama3.2:1b"
```

and ensure Ollama is running:

```bash
ollama serve
```

---

## Error: Python 3.9 incompatibility

CrewAI requires Python 3.10+.

Verify:

```bash
python3.11 --version
```

---

# Future Improvements

Potential future extensions include:
- live airline API integrations,
- reinforcement learning,
- autonomous booking execution,
- browser automation,
- time-series forecasting,
- cross-currency normalization,
- personalized traveler preference modeling,
- dynamic retraining pipelines.

---

# Research Context

The project draws inspiration from:
- airline price prediction research,
- Buy/Wait classification systems,
- travel recommendation systems,
- agentic AI workflows,
- human-in-the-loop decision systems.

The primary contribution is integrating:
- prediction,
- reasoning,
- and execution support

into a unified multi-agent workflow for travel price intelligence.

---

# License

Educational and research prototype only.
Not intended for production deployment.