"""
Prediction Engine for TravelWatch AI
Loads pre-trained models and generates buy/wait recommendations
"""

import json
import os
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

# IATA ↔ training-data city name mapping (Indian domestic routes)
IATA_TO_CITY = {
    "BLR": "Bangalore", "MAA": "Chennai", "DEL": "Delhi",
    "HYD": "Hyderabad", "CCU": "Kolkata", "BOM": "Mumbai",
}
_INDIAN_IATA = frozenset(IATA_TO_CITY.keys())
_INDIAN_CITIES = frozenset(IATA_TO_CITY.values())


def _price_change_by_days(days_left: float) -> float:
    """
    Expected price change % as a function of days until departure.
    Based on typical airline pricing dynamics (any route).
    Positive = price will rise, negative = price may still drop.
    """
    if days_left >= 60:
        return -5.0   # Early booking — prices often still falling
    elif days_left >= 30:
        return 8.0    # Moderate rise starting
    elif days_left >= 14:
        return 20.0   # Significant increase
    return 38.0       # Last-minute premium


class PredictionEngine:
    """
    Inference engine for price prediction and buy/wait classification.
    
    - Loads Ridge regression model for price prediction
    - Loads Logistic Regression model for BUY/WAIT classification
    - Handles feature engineering and normalization
    """
    
    def __init__(self):
        """Initialize and load model weights from JSON"""
        self.model_data = None
        self.reg_model = None
        self.clf_model = None
        self.feature_stats = None
        self._load_models()
    
    def _load_models(self):
        """Load model data from JSON file"""
        base_dir = os.path.dirname(__file__)
        model_path = os.path.join(base_dir, "model_weights", "travelwatch_models.json")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model weights not found at {model_path}")
        
        with open(model_path, "r") as f:
            self.model_data = json.load(f)
        
        self.reg_model = self.model_data.get("regression", {})
        self.clf_model = self.model_data.get("classification", {})
    
    # ───────────────────────────────────────────────────────────────────────────
    # Feature Engineering
    # ───────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _resolve_city(name: str) -> str:
        """Resolve IATA code → training city name, or pass city name through."""
        return IATA_TO_CITY.get(name.upper(), name)

    def _get_flight_duration(self, origin: str, dest: str) -> float:
        """
        Estimate flight duration in hours based on route.
        Returns normalized duration (0-1 scale, roughly).
        
        Training data shows India domestic routes:
        - Bangalore-Chennai: ~1.0 hour
        - Bangalore-Delhi: ~2.5 hours
        - Bangalore-Hyderabad: ~1.5 hours
        - Delhi-Mumbai: ~1.5 hours
        - Mumbai-Chennai: ~1.5 hours
        """
        # Route pairs and typical duration in hours (India flights)
        route_durations = {
            ("Bangalore", "Chennai"): 1.0,
            ("Bangalore", "Delhi"): 2.5,
            ("Bangalore", "Hyderabad"): 1.5,
            ("Bangalore", "Kolkata"): 2.5,
            ("Bangalore", "Mumbai"): 1.5,
            ("Chennai", "Delhi"): 2.5,
            ("Chennai", "Hyderabad"): 1.5,
            ("Chennai", "Kolkata"): 2.0,
            ("Chennai", "Mumbai"): 1.5,
            ("Delhi", "Hyderabad"): 1.5,
            ("Delhi", "Kolkata"): 2.0,
            ("Delhi", "Mumbai"): 1.5,
            ("Hyderabad", "Kolkata"): 2.0,
            ("Hyderabad", "Mumbai"): 1.5,
            ("Kolkata", "Mumbai"): 2.5,
        }
        
        o, d = self._resolve_city(origin), self._resolve_city(dest)
        duration = route_durations.get((o, d)) or route_durations.get((d, o))
        if duration is None:
            duration = 2.0  # Default estimate
        
        # Normalize to 0-1 range (training data range was roughly 0-4 hours)
        return duration / 4.0
    
    def _get_days_left(self, dep_date: str) -> float:
        """
        Calculate days until departure.
        Returns normalized days_left (0-1 scale).
        
        Training data suggests route bookings from 1-60 days in advance.
        """
        try:
            if isinstance(dep_date, str):
                dep_dt = datetime.strptime(dep_date, "%Y-%m-%d").date()
            else:
                dep_dt = dep_date
            
            today = datetime.now().date()
            days = (dep_dt - today).days
            days = max(1, min(days, 60))  # Clamp to 1-60 range
            
            # Normalize to 0-1 range
            return days / 60.0
        except Exception as e:
            print(f"Error calculating days_left: {e}")
            return 0.5  # Default to middle value
    
    def _encode_feature_vector(self, flight_data: dict) -> np.ndarray:
        """
        Encode flight data into feature vector for regression model.
        
        Expected regression features (38 total):
        - duration
        - days_left
        - airline_* (6 airlines)
        - source_city_* (6 cities)
        - destination_city_* (6 cities)
        - departure_time_* (6 times)
        - arrival_time_* (6 times)
        - class_* (2: Business, Economy)
        - stops_* (3: zero, one, two_or_more)
        """
        # Extract data — resolve IATA codes to city names used in training
        origin = self._resolve_city(flight_data.get("origin", "Delhi"))
        dest = self._resolve_city(flight_data.get("destination", "Mumbai"))
        airline = flight_data.get("airline")
        dep_date = flight_data.get("dep_date")
        class_type = flight_data.get("class", "Economy")
        stops = flight_data.get("stops", 0)  # 0, 1, 2+
        dep_time = flight_data.get("departure_time", "Morning")
        arr_time = flight_data.get("arrival_time", "Afternoon")
        
        # Duration and days_left
        duration = self._get_flight_duration(origin, dest)
        days_left = self._get_days_left(dep_date)
        
        features = [duration, days_left]
        
        # Airline encoding. Unknown/Any means no airline filter, so use an even
        # distribution instead of biasing the prediction toward one carrier.
        airlines = ["AirAsia", "Air_India", "GO_FIRST", "Indigo", "SpiceJet", "Vistara"]
        if airline in airlines:
            features.extend(1.0 if airline == a else 0.0 for a in airlines)
        else:
            features.extend([1.0 / len(airlines)] * len(airlines))
        
        # Source city encoding (6 cities)
        cities = ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]
        for city in cities:
            features.append(1.0 if origin == city else 0.0)
        
        # Destination city encoding (6 cities)
        for city in cities:
            features.append(1.0 if dest == city else 0.0)
        
        # Departure time encoding (6 times)
        dep_times = ["Afternoon", "Early_Morning", "Evening", "Late_Night", "Morning", "Night"]
        for t in dep_times:
            features.append(1.0 if dep_time == t else 0.0)
        
        # Arrival time encoding (6 times)
        for t in dep_times:
            features.append(1.0 if arr_time == t else 0.0)
        
        # Class encoding (2: Business, Economy)
        features.append(1.0 if class_type == "Business" else 0.0)
        features.append(1.0 if class_type == "Economy" else 0.0)
        
        # Stops encoding (3: zero, one, two_or_more)
        features.append(1.0 if stops == 0 else 0.0)
        features.append(1.0 if stops == 1 else 0.0)
        features.append(1.0 if stops >= 2 else 0.0)
        
        return np.array(features, dtype=float)
    
    def _standardize_features(self, X: np.ndarray) -> np.ndarray:
        """
        Standardize feature vector before prediction.
        Training used: X_new = (X - mean) / std
        
        Note: We use approximate standardization based on training data ranges.
        """
        # Feature-wise standardization (approximate values from training)
        # For simplicity, we normalize continuous features and leave one-hot as-is
        X_std = X.copy()
        
        # Normalize continuous features (indices 0-1): duration, days_left
        X_std[0] = (X_std[0] - 0.5) / 0.289  # Approx mean=0.5, std=0.289
        X_std[1] = (X_std[1] - 0.5) / 0.289
        
        return X_std
    
    def _encode_class_features(self, flight_data: dict) -> np.ndarray:
        """
        Encode flight data for classification model (BUY/WAIT).
        
        Classification features (7 total, standardized):
        - duration
        - days_left
        - class_Business
        - class_Economy
        - stops_one
        - stops_two_or_more
        - stops_zero
        """
        origin = self._resolve_city(flight_data.get("origin", "Delhi"))
        dest = self._resolve_city(flight_data.get("destination", "Mumbai"))
        dep_date = flight_data.get("dep_date")
        class_type = flight_data.get("class", "Economy")
        stops = flight_data.get("stops", 0)

        duration = self._get_flight_duration(origin, dest)
        days_left = self._get_days_left(dep_date)
        
        features = [
            duration,
            days_left,
            1.0 if class_type == "Business" else 0.0,
            1.0 if class_type == "Economy" else 0.0,
            1.0 if stops == 1 else 0.0,
            1.0 if stops >= 2 else 0.0,
            1.0 if stops == 0 else 0.0,
        ]
        
        return np.array(features, dtype=float)
    
    # ───────────────────────────────────────────────────────────────────────────
    # Model Predictions
    # ───────────────────────────────────────────────────────────────────────────
    
    def _sigmoid(self, z: float) -> float:
        """Sigmoid activation function"""
        z = np.clip(z, -500, 500)
        return 1.0 / (1.0 + np.exp(-z))
    
    def predict_price(self, flight_data: dict) -> dict:
        """
        Predict flight price using Ridge regression model.
        
        Args:
            flight_data: dict with keys like origin, destination, dep_date, class, etc.
        
        Returns:
            dict with predicted_price, confidence, model_name
        """
        try:
            # Get model weights
            ridge_data = self.reg_model.get("ridge", {})
            W = np.array(ridge_data.get("W", []), dtype=float)
            
            if len(W) == 0:
                raise ValueError("Ridge model weights not found")
            
            # Encode features
            X = self._encode_feature_vector(flight_data)
            X_std = self._standardize_features(X)
            
            # Add bias term (1 at the beginning)
            X_with_bias = np.concatenate([[1], X_std])
            
            # Prediction: y = X @ W
            predicted_price = float(np.dot(X_with_bias, W))
            predicted_price = max(100, predicted_price)  # Ensure reasonable price
            
            # Get R² for confidence (Ridge R² ≈ 0.913)
            r2 = ridge_data.get("r2", 0.91)
            confidence = int(r2 * 100)
            
            return {
                "predicted_price": predicted_price,
                "confidence": confidence,
                "model": "Ridge Regression",
                "r2": r2
            }
        except Exception as e:
            print(f"Error in predict_price: {e}")
            return {
                "predicted_price": flight_data.get("current_price", 500),
                "confidence": 0,
                "model": "Error",
                "error": str(e)
            }
    
    def predict_buy_wait(self, flight_data: dict) -> dict:
        """
        Predict BUY/WAIT recommendation using Logistic Regression.
        
        Args:
            flight_data: dict with flight information
        
        Returns:
            dict with recommendation (BUY/WAIT), confidence, probability
        """
        try:
            # Get model weights
            lr_data = self.clf_model.get("logistic_regression", {})
            W = np.array(lr_data.get("W", []), dtype=float)
            b = float(lr_data.get("b", 0.0))
            
            if len(W) == 0:
                raise ValueError("Logistic Regression weights not found")
            
            # Encode features
            X = self._encode_class_features(flight_data)
            X_std = self._standardize_features(X)
            
            # Prediction: sigmoid(X @ W + b)
            logit = np.dot(X_std, W) + b
            probability = self._sigmoid(logit)
            
            # Threshold at 0.5 for BUY/WAIT
            recommendation = "BUY" if probability >= 0.5 else "WAIT"
            confidence = int(probability * 100) if probability >= 0.5 else int((1 - probability) * 100)
            
            # Get model performance metrics
            auc = lr_data.get("auc", 0.996)
            f1 = lr_data.get("f1", 0.993)
            
            return {
                "recommendation": recommendation,
                "confidence": confidence,
                "probability": float(probability),
                "model": "Logistic Regression",
                "auc": auc,
                "f1": f1
            }
        except Exception as e:
            print(f"Error in predict_buy_wait: {e}")
            return {
                "recommendation": "WAIT",
                "confidence": 0,
                "probability": 0.5,
                "model": "Error",
                "error": str(e)
            }
    
    def generate_recommendation(self, flight_data: dict) -> dict:
        """
        Generate complete recommendation combining price prediction and buy/wait classification.
        
        Args:
            flight_data: dict with flight information and current_price
        
        Returns:
            dict with all recommendation details
        """
        buy_wait_pred = self.predict_buy_wait(flight_data)  # universal (no city features)

        current_price = float(flight_data.get("current_price", 0) or 0)
        target_price = float(flight_data.get("target", 0) or current_price)

        raw_origin = flight_data.get("origin", "")
        raw_dest = flight_data.get("destination", "")
        is_indian = (
            (raw_origin.upper() in _INDIAN_IATA or raw_origin in _INDIAN_CITIES) and
            (raw_dest.upper() in _INDIAN_IATA or raw_dest in _INDIAN_CITIES)
        )

        if is_indian:
            # Use Ridge regression trained on Indian domestic data
            price_pred = self.predict_price(flight_data)
            predicted_price = price_pred.get("predicted_price", current_price)
            reg_meta = {
                "name": price_pred["model"],
                "confidence": price_pred["confidence"],
                "r2": price_pred.get("r2", 0),
            }
        else:
            # Universal heuristic: prices rise as departure approaches
            days_norm = self._get_days_left(flight_data.get("dep_date", ""))
            pct = _price_change_by_days(days_norm * 60)
            predicted_price = current_price * (1 + pct / 100) if current_price > 0 else 0
            reg_meta = {"name": "Days-to-Departure Heuristic", "confidence": 72, "r2": 0}

        price_change = ((predicted_price - current_price) / current_price * 100) if current_price > 0 else 0
        change_direction = "down" if price_change < 0 else "up"

        return {
            "recommendation": buy_wait_pred["recommendation"],
            "confidence": buy_wait_pred["confidence"],
            "change_pct": round(abs(price_change), 1),
            "change_dir": change_direction,
            "predicted_price": round(predicted_price, 2),
            "current_price": round(current_price, 2),
            "target": round(target_price, 2),
            "price_advantage": round(target_price - current_price, 2),
            "models": {
                "regression": reg_meta,
                "classification": {
                    "name": buy_wait_pred["model"],
                    "auc": buy_wait_pred.get("auc", 0),
                    "f1": buy_wait_pred.get("f1", 0),
                },
            },
        }


# Global engine instance
_engine = None

def get_prediction_engine() -> PredictionEngine:
    """Get or initialize the global prediction engine"""
    global _engine
    if _engine is None:
        _engine = PredictionEngine()
    return _engine


def predict_flight(flight_data: dict) -> dict:
    """
    Convenience function to generate recommendation for a flight.
    
    Args:
        flight_data: dict with keys:
            - origin: str (e.g., "Delhi")
            - destination: str (e.g., "Mumbai")
            - dep_date: str or date (e.g., "2026-05-20")
            - current_price: float
            - target: float (optional)
            - class: str (default "Economy")
            - airline: str (optional filter; omitted means any airline)
            - stops: int (default 0)
            - departure_time: str (optional)
            - arrival_time: str (optional)
    
    Returns:
        dict with recommendation and confidence
    """
    engine = get_prediction_engine()
    return engine.generate_recommendation(flight_data)
