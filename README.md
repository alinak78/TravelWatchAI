# TravelWatchAI

INFO 5368 Final Project — Flight Price Prediction + BUY/WAIT Multi-Agent System

---

# Project Overview

TravelWatchAI is a machine learning and AI-agent powered travel price intelligence platform that helps users decide whether to BUY or WAIT for airline tickets.

Instead of only showing current prices, the system combines:
- real-time flight pricing,
- machine learning prediction,
- Buy/Wait classification,
- anomaly detection,
- and agent-based reasoning

to support travel booking decisions under uncertainty.

The platform integrates:
- regression models for future price prediction,
- classification models for BUY/WAIT recommendation,
- Streamlit for interactive visualization,
- and CrewAI agents for AI-driven workflow orchestration.

The application focuses on the core problem of airline price volatility:
users often do not know whether current prices are likely to increase or decrease closer to departure.

TravelWatchAI transforms raw pricing data into:
- interpretable recommendations,
- confidence scores,
- future price estimates,
- and booking decision support.

---

# Key Features

- Flight price prediction
- BUY/WAIT recommendation engine
- Multi-agent AI workflow
- Real-time Skyscanner pricing
- Ridge / Lasso / Logistic Regression models
- KNN classification baseline
- Streamlit dashboard
- Route comparison system
- AI-agent explanation page
- Interactive ML insights and evaluation metrics
- Human-in-the-loop booking support

---

# Dataset

Download `Clean_Dataset.csv` from Kaggle:

[Flight Price Prediction Dataset](https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction?utm_source=chatgpt.com)

Place it at:

```text
datasets/Clean_Dataset.csv
```

---

# Project Structure

```text
TRAVELWATCHAI/
│
├── ai_agent/
│   ├── crew.py
│   ├── streamlit_bridge.py
│   ├── README.md
│   └── requirements.txt
│
├── datasets/
│   └── Clean_Dataset.csv
│
├── document_reference/
│   └── PAML_Proposal.pdf
│
├── notebooks/
│   └── travelwatchai.ipynb
│
├── streamlit_app/
│   ├── views/
│   │   ├── dashboard.py
│   │   ├── add_watch.py
│   │   ├── compare.py
│   │   ├── task_detail.py
│   │   ├── ml_insights.py
│   │   ├── ai_agent.py
│   │   └── settings.py
│   │
│   ├── model_weights/
│   │
│   ├── app.py
│   ├── prediction_engine.py
│   ├── skyscanner_api.py
│   └── airports_db.py
│
├── requirements.txt
└── README.md
```

---

# Machine Learning Workflow

Notebook path:

```text
notebooks/travelwatchai.ipynb
```

Additional methodology details may be found in:

```text
document_reference/PAML_Proposal.pdf
```

---

## Data Processing Pipeline

1. Load and clean `Clean_Dataset.csv`
2. Handle missing values
3. Encode categorical variables
4. Normalize numeric features
5. Remove outliers using:
   - IQR filtering
   - Z-score detection
6. Create engineered BUY/WAIT labels

---

## Regression Models

Used for future price prediction:

- Linear Regression
- Polynomial Regression
- Ridge Regression
- Lasso Regression

Evaluation metrics:
- MSE
- RMSE
- MAE
- R²

Ridge Regression was selected as the primary deployment model because it provided stable performance while reducing overfitting.

---

## Classification Models

Used for BUY/WAIT recommendation:

- Logistic Regression
- KNN Classification

Evaluation metrics:
- Accuracy
- F1 Score
- AUC-ROC

Logistic Regression was selected as the primary deployment classifier due to:
- strong performance,
- interpretability,
- lower computational cost,
- and greater stability relative to KNN.

---

# AI Agent Workflow

The AI-agent system decomposes travel decision-making into specialized stages.

## 1. Watch Task Parser

Converts natural-language requests into structured watch tasks.

Example:

```text
DEL to BOM on 2026-05-20 under 5500 INR economy
```

Extracted fields:
- origin
- destination
- travel dates
- target price
- currency
- cabin class
- passenger count

---

## 2. Fare Aggregation

Retrieves:
- live Skyscanner prices,
- fallback estimates if APIs fail,
- normalized route-level pricing.

---

## 3. ML Analysis

Applies:
- regression prediction,
- BUY/WAIT classification,
- confidence scoring,
- expected price movement estimation.

---

## 4. Recommendation Layer

Outputs:
- BUY or WAIT recommendation
- confidence score
- predicted future price
- booking/search link
- AI-generated reasoning summary

---

# Create Environment in WSL

The project was primarily developed and tested inside Ubuntu/WSL.

```bash
cd /home/flyingc/TravelWatchAI

python3 -m venv .venv-travelwatch

source .venv-travelwatch/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt
```

Install JupyterLab:

```bash
pip install jupyterlab
```

---

# Run Notebook

```bash
source .venv-travelwatch/bin/activate

jupyter lab
```

---

# Run the Streamlit App

```bash
source .venv-travelwatch/bin/activate

cd streamlit_app

streamlit run app.py
```

---

# App Pages

## Dashboard
Overview cards for:
- recent watches,
- current prices,
- BUY/WAIT recommendations,
- booking links,
- multi-route charts.

---

## Add New Watch
Create route monitoring tasks with:
- origin,
- destination,
- dates,
- target price,
- cabin class,
- passengers,
- optional stop/time preferences.

---

## Compare
Compare up to three routes simultaneously:
- current prices,
- predicted prices,
- BUY/WAIT recommendation,
- estimated savings.

---

## Task Detail
Detailed route-level analysis:
- recommendation reasoning,
- price history,
- top itineraries,
- booking actions.

---

## ML Insights
Interactive evaluation dashboards:
- F1 Score
- AUC-ROC
- confusion matrix
- ROC curves
- R²
- RMSE
- MAE
- learning curves

---

## View Data
Dataset exploration tools:
- raw data preview
- processed features
- missing values
- feature distributions
- correlation heatmaps

---

## AI Agent
CrewAI-powered multi-agent workflow demonstration:
- natural language travel requests
- structured parsing
- ML-based recommendation reasoning
- AI-generated decision summaries

---

# API Configuration

Create:

```text
streamlit_app/.streamlit/secrets.toml
```

Add:

```toml
RAPIDAPI_KEY = "your_api_key"
```

You may also set:

```bash
export RAPIDAPI_KEY="your_api_key"
```

---

# Technologies Used

## Frameworks
- Streamlit
- CrewAI
- Ollama
- LiteLLM

## ML Libraries
- scikit-learn
- pandas
- NumPy

## APIs
- Skyscanner RapidAPI

## Visualization
- Plotly
- Matplotlib

---

# Future Improvements

Potential future extensions include:
- autonomous booking execution,
- reinforcement learning,
- browser automation,
- dynamic retraining pipelines,
- cross-currency normalization,
- personalized traveler profiles,
- time-series forecasting,
- and multi-modal AI travel assistants.

---

# License

Educational and research prototype only.
Not intended for commercial deployment.

