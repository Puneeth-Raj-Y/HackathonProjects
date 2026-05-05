"""
ML Model Training Script with Synthetic Dataset
Trains Isolation Forest model for fraud detection
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import pickle
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ml.fraud_detector import FraudDetectionEngine


def generate_synthetic_dataset(n_normal: int = 800, n_anomaly: int = 100) -> np.ndarray:
    """
    Generate synthetic transaction data for training
    
    Args:
        n_normal: Number of normal transactions
        n_anomaly: Number of anomalous transactions
        
    Returns:
        numpy array of features
    """
    print(f"Generating synthetic dataset: {n_normal} normal, {n_anomaly} anomalies...")

    features_list = []

    # Normal transactions
    for _ in range(n_normal):
        quantity = np.random.normal(loc=15.0, scale=5.0)  # Normal: ~15kg
        frequency = np.random.normal(loc=0.5, scale=0.2)  # Normal: ~0.5 transactions/day
        time_gap = np.random.exponential(scale=24)  # ~24 hours between transactions
        deviation = np.random.normal(loc=0.1, scale=0.1)  # Low deviation
        hour = np.random.uniform(0, 24)  # Any hour
        day_of_week = np.random.uniform(0, 7)

        features = [
            max(0, quantity),  # Ensure positive
            max(0.01, frequency),
            max(0.5, time_gap),
            max(0, deviation),
            hour,
            day_of_week
        ]
        features_list.append(features)

    # Anomalous transactions
    for _ in range(n_anomaly):
        # Anomaly Type 1: Very high quantity
        if np.random.random() < 0.3:
            quantity = np.random.uniform(80, 200)  # Very high
            frequency = np.random.uniform(1, 3)
            time_gap = np.random.uniform(0.5, 2)  # Very short interval
            deviation = np.random.uniform(2, 5)  # High deviation
            
        # Anomaly Type 2: Too frequent transactions
        elif np.random.random() < 0.6:
            quantity = np.random.uniform(5, 25)
            frequency = np.random.uniform(3, 10)  # Very frequent
            time_gap = np.random.uniform(0.5, 5)  # Short intervals
            deviation = np.random.uniform(0.5, 2)
            
        # Anomaly Type 3: Unusual patterns
        else:
            quantity = np.random.uniform(30, 150)
            frequency = np.random.uniform(0.1, 1)
            time_gap = np.random.uniform(0.1, 0.5)  # Extremely short
            deviation = np.random.uniform(3, 10)

        hour = np.random.choice([2, 3, 4, 5])  # Unusual hours (early morning)
        day_of_week = np.random.choice([0, 6])  # Weekends

        features = [quantity, frequency, time_gap, deviation, hour, day_of_week]
        features_list.append(features)

    return np.array(features_list)


def train_fraud_detection_model(output_dir: str = 'backend/ml/models'):
    """
    Train fraud detection model and save it
    
    Args:
        output_dir: Directory to save the model
    """
    os.makedirs(output_dir, exist_ok=True)

    # Generate synthetic dataset
    X_train = generate_synthetic_dataset(n_normal=800, n_anomaly=100)

    print(f"\nTraining Isolation Forest model...")
    print(f"Dataset shape: {X_train.shape}")
    print(f"Features: [quantity, frequency, time_gap, deviation, hour, day_of_week]")

    # Train Isolation Forest
    model = IsolationForest(
        contamination=0.1,  # Expect 10% anomalies
        random_state=42,
        n_estimators=100
    )

    model.fit(X_train)

    # Save model
    model_path = os.path.join(output_dir, 'fraud_detection_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"✓ Model trained and saved to: {model_path}")

    # Evaluate on synthetic data
    predictions = model.predict(X_train)
    n_anomalies = np.sum(predictions == -1)
    n_normals = np.sum(predictions == 1)

    print(f"\nModel Evaluation on Training Data:")
    print(f"  Detected anomalies: {n_anomalies}")
    print(f"  Detected normal: {n_normals}")
    print(f"  Anomaly rate: {n_anomalies / len(predictions) * 100:.2f}%")

    # Test with sample transactions
    print(f"\n\nTesting with sample transactions:")
    fraud_engine = FraudDetectionEngine(model_path)

    # Sample normal transaction
    normal_txn = {
        'quantity': 12.0,
        'frequency': 0.3,
        'time_gap_hours': 48,
        'avg_quantity': 15.0,
        'hour': 10,
        'day_of_week': 2,
        'stock_available': 100.0
    }

    result = fraud_engine.predict_fraud(normal_txn)
    print(f"\n  Normal transaction:")
    print(f"    Risk Score: {result['risk_score']:.2f}")
    print(f"    Is Fraud: {result['is_fraud']}")
    print(f"    Reason: {result['reason']}")

    # Sample fraudulent transaction
    fraud_txn = {
        'quantity': 150.0,
        'frequency': 5.0,
        'time_gap_hours': 0.5,
        'avg_quantity': 15.0,
        'hour': 3,
        'day_of_week': 6,
        'stock_available': 100.0
    }

    result = fraud_engine.predict_fraud(fraud_txn)
    print(f"\n  Fraudulent transaction:")
    print(f"    Risk Score: {result['risk_score']:.2f}")
    print(f"    Is Fraud: {result['is_fraud']}")
    print(f"    Reason: {result['reason']}")

    return model_path


if __name__ == '__main__':
    model_path = train_fraud_detection_model()
    print(f"\n✓ Training complete! Model ready at: {model_path}")
