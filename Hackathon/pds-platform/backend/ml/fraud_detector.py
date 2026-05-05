"""
Fraud Detection Module using Isolation Forest and Rule-based Checks
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pickle
import os


class FraudDetectionEngine:
    """
    ML-based fraud detection using Isolation Forest with rule-based checks.
    Detects anomalies in transactions and returns risk scores.
    """

    def __init__(self, model_path: str = None):
        """
        Initialize Fraud Detection Engine
        
        Args:
            model_path: Path to pre-trained model pickle file
        """
        self.model = None
        self.scaler_stats = None
        self.rules_config = {
            'duplicate_time_window': 300,  # 5 minutes in seconds
            'max_transactions_per_day': 2,
            'max_quantity_per_transaction': 50.0,
            'min_time_between_transactions': 60,  # seconds
        }
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def extract_features(self, transaction_data: Dict) -> np.ndarray:
        """
        Extract features from transaction for ML model
        
        Args:
            transaction_data: Dictionary with transaction details
            
        Returns:
            numpy array of features
        """
        features = []

        # Feature 1: Transaction quantity
        quantity = float(transaction_data.get('quantity', 0))
        features.append(quantity)

        # Feature 2: Transaction frequency (transactions per day)
        frequency = float(transaction_data.get('frequency', 0))
        features.append(frequency)

        # Feature 3: Time gap from last transaction (hours)
        time_gap = float(transaction_data.get('time_gap_hours', 24))
        features.append(time_gap)

        # Feature 4: Deviation from average usage (percentage)
        avg_quantity = float(transaction_data.get('avg_quantity', 1))
        deviation = abs(quantity - avg_quantity) / max(avg_quantity, 1)
        features.append(deviation)

        # Feature 5: Hour of transaction (cyclical pattern)
        hour = float(transaction_data.get('hour', 12))
        features.append(hour)

        # Feature 6: Day of week (cyclical pattern)
        day_of_week = float(transaction_data.get('day_of_week', 0))
        features.append(day_of_week)

        return np.array(features).reshape(1, -1)

    def apply_rule_based_checks(self, transaction_data: Dict, 
                               user_history: List[Dict]) -> Tuple[float, str]:
        """
        Apply rule-based fraud checks
        
        Args:
            transaction_data: Current transaction details
            user_history: List of user's previous transactions
            
        Returns:
            Tuple of (risk_score, reason)
        """
        risk_score = 0.0
        reasons = []

        # Rule 1: Duplicate usage within short time window
        if user_history:
            last_transaction = user_history[-1]
            time_diff = (datetime.utcnow() - last_transaction.get('timestamp', datetime.utcnow())).total_seconds()
            
            if time_diff < self.rules_config['min_time_between_transactions']:
                risk_score += 0.3
                reasons.append("Duplicate usage within short time")

        # Rule 2: Abnormal high distribution
        quantity = transaction_data.get('quantity', 0)
        if quantity > self.rules_config['max_quantity_per_transaction']:
            risk_score += 0.25
            reasons.append(f"High quantity: {quantity} exceeds max {self.rules_config['max_quantity_per_transaction']}")

        # Rule 3: Multiple transactions in single day
        today_transactions = [
            t for t in user_history
            if (datetime.utcnow() - t.get('timestamp', datetime.utcnow())).days == 0
        ]
        
        if len(today_transactions) >= self.rules_config['max_transactions_per_day']:
            risk_score += 0.2
            reasons.append(f"Multiple transactions ({len(today_transactions)}) in single day")

        # Rule 4: Stock mismatch detection
        stock_available = transaction_data.get('stock_available', quantity)
        if quantity > stock_available * 1.1:  # 10% tolerance
            risk_score += 0.25
            reasons.append("Stock mismatch: requesting more than available")

        return min(risk_score, 1.0), " | ".join(reasons) if reasons else "No rule violations"

    def predict_fraud(self, transaction_data: Dict, 
                      user_history: List[Dict] = None) -> Dict:
        """
        Predict if transaction is fraudulent
        
        Args:
            transaction_data: Transaction details
            user_history: List of user's previous transactions
            
        Returns:
            Dictionary with fraud assessment
        """
        if user_history is None:
            user_history = []

        # Extract features for ML model
        features = self.extract_features(transaction_data)

        # Get ML prediction
        ml_risk_score = 0.0
        is_anomaly = 0
        ml_reason = "Normal transaction"

        if self.model:
            prediction = self.model.predict(features)[0]
            anomaly_score = self.model.score_samples(features)[0]
            
            # Normalize anomaly score to 0-1 range
            ml_risk_score = 1.0 / (1.0 + np.exp(anomaly_score))
            is_anomaly = 1 if prediction == -1 else 0
            
            if is_anomaly:
                ml_reason = f"Anomaly detected (score: {ml_risk_score:.2f})"

        # Apply rule-based checks
        rule_risk_score, rule_reason = self.apply_rule_based_checks(
            transaction_data, 
            user_history
        )

        # Combine scores (weighted average)
        final_risk_score = (ml_risk_score * 0.6 + rule_risk_score * 0.4)

        # Determine if transaction should be flagged
        is_flagged = final_risk_score > 0.5 or is_anomaly

        result = {
            'is_fraud': is_flagged,
            'risk_score': min(final_risk_score, 1.0),
            'ml_risk_score': ml_risk_score,
            'rule_risk_score': rule_risk_score,
            'is_anomaly': is_anomaly,
            'ml_reason': ml_reason,
            'rule_reason': rule_reason,
            'reason': f"ML: {ml_reason} | Rules: {rule_reason}",
            'confidence': 'high' if final_risk_score > 0.7 else 'medium' if final_risk_score > 0.5 else 'low'
        }

        return result

    def train_model(self, X_train: np.ndarray, contamination: float = 0.1):
        """
        Train Isolation Forest model
        
        Args:
            X_train: Training features
            contamination: Expected proportion of anomalies
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.model.fit(X_train)

    def save_model(self, model_path: str):
        """Save model to pickle file"""
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, model_path: str):
        """Load model from pickle file"""
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

    def batch_predict(self, transactions: List[Dict]) -> List[Dict]:
        """
        Predict fraud for multiple transactions
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            List of fraud assessment results
        """
        results = []
        for transaction in transactions:
            result = self.predict_fraud(transaction)
            results.append(result)
        return results
