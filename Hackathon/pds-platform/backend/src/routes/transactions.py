"""
Beneficiary Transaction Routes with Fraud Detection
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.db import SessionLocal
from models import User, Shop, BeneficiaryTransaction, FraudAlert, UserRole
from utils.auth_utils import get_token_from_request, verify_access_token

transactions_bp = Blueprint('transactions', __name__)


def require_auth(func):
    """Decorator to verify authentication token"""
    def wrapper(*args, **kwargs):
        token = get_token_from_request(request)
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401
        
        payload = verify_access_token(token)
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401
        
        request.user_id = payload['user_id']
        request.user_role = payload['role']
        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return wrapper


def get_fraud_detector():
    """Get fraud detection engine instance"""
    try:
        from ml.fraud_detector import FraudDetectionEngine
        model_path = 'backend/ml/models/fraud_detection_model.pkl'
        return FraudDetectionEngine(model_path)
    except:
        return None


@transactions_bp.route('/distribute', methods=['POST'])
@require_auth
def distribute_goods():
    """
    Distribute goods to beneficiary
    
    Expected JSON:
    {
        "user_id": 1,
        "shop_id": 1,
        "quantity": 10.0
    }
    """
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'shop_id', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        db: Session = SessionLocal()
        
        # Verify user exists and is beneficiary
        user = db.query(User).filter(User.id == data['user_id']).first()
        if not user:
            db.close()
            return jsonify({'error': 'User not found'}), 404

        if user.role != UserRole.BENEFICIARY:
            db.close()
            return jsonify({'error': 'Only beneficiaries can receive distributions'}), 403

        # Verify shop exists
        shop = db.query(Shop).filter(Shop.id == data['shop_id']).first()
        if not shop:
            db.close()
            return jsonify({'error': 'Shop not found'}), 404

        quantity = float(data['quantity'])

        # Check stock availability
        if shop.current_stock < quantity:
            db.close()
            return jsonify({
                'error': 'Insufficient stock',
                'available': shop.current_stock,
                'requested': quantity
            }), 400

        # Get user transaction history for fraud detection
        user_history = db.query(BeneficiaryTransaction).filter(
            BeneficiaryTransaction.user_id == data['user_id']
        ).order_by(BeneficiaryTransaction.timestamp.desc()).limit(10).all()

        # Prepare fraud detection features
        last_transaction_time = None
        if user_history:
            last_transaction_time = user_history[0].timestamp
        
        time_gap_hours = 24
        if last_transaction_time:
            time_gap_hours = (datetime.utcnow() - last_transaction_time).total_seconds() / 3600

        # Calculate user statistics
        user_transactions_today = len([
            t for t in user_history
            if (datetime.utcnow() - t.timestamp).days == 0
        ])

        avg_quantity = 0
        if user_history:
            avg_quantity = sum(t.quantity for t in user_history) / len(user_history)
        else:
            avg_quantity = quantity

        # Fraud detection
        fraud_detector = get_fraud_detector()
        fraud_risk = {
            'is_fraud': False,
            'risk_score': 0.0,
            'reason': 'No fraud detector available'
        }

        if fraud_detector:
            transaction_data = {
                'quantity': quantity,
                'frequency': user_transactions_today + 1,
                'time_gap_hours': time_gap_hours,
                'avg_quantity': avg_quantity,
                'hour': datetime.utcnow().hour,
                'day_of_week': datetime.utcnow().weekday(),
                'stock_available': shop.current_stock
            }

            fraud_risk = fraud_detector.predict_fraud(
                transaction_data,
                [{'timestamp': t.timestamp, 'quantity': t.quantity} for t in user_history]
            )

        # Create transaction
        beneficiary_txn = BeneficiaryTransaction(
            user_id=data['user_id'],
            shop_id=data['shop_id'],
            quantity=quantity
        )

        db.add(beneficiary_txn)
        db.flush()  # Flush to get transaction ID

        # Create fraud alert if detected
        if fraud_risk['is_fraud']:
            fraud_alert = FraudAlert(
                beneficiary_transaction_id=beneficiary_txn.id,
                reason=fraud_risk['reason'],
                risk_score=fraud_risk['risk_score'],
                is_anomaly=fraud_risk.get('is_anomaly', 0)
            )
            db.add(fraud_alert)

        # Update shop stock
        shop.current_stock -= quantity

        db.commit()
        txn_id = beneficiary_txn.id
        db.close()

        return jsonify({
            'message': 'Distribution completed',
            'transaction_id': txn_id,
            'user_id': data['user_id'],
            'shop_id': data['shop_id'],
            'quantity': quantity,
            'fraud_risk': {
                'is_fraud': fraud_risk['is_fraud'],
                'risk_score': fraud_risk['risk_score'],
                'reason': fraud_risk['reason'],
                'confidence': fraud_risk.get('confidence', 'low')
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transactions_bp.route('/all', methods=['GET'])
@require_auth
def get_transactions():
    """Get all beneficiary transactions"""
    try:
        user_id = request.args.get('user_id', type=int)
        shop_id = request.args.get('shop_id', type=int)
        limit = request.args.get('limit', 100, type=int)

        db: Session = SessionLocal()
        
        query = db.query(BeneficiaryTransaction)
        
        if user_id:
            query = query.filter(BeneficiaryTransaction.user_id == user_id)
        
        if shop_id:
            query = query.filter(BeneficiaryTransaction.shop_id == shop_id)

        transactions = query.order_by(
            BeneficiaryTransaction.timestamp.desc()
        ).limit(limit).all()

        db.close()

        return jsonify({
            'count': len(transactions),
            'transactions': [
                {
                    'id': t.id,
                    'user_id': t.user_id,
                    'shop_id': t.shop_id,
                    'quantity': t.quantity,
                    'timestamp': t.timestamp.isoformat()
                }
                for t in transactions
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transactions_bp.route('/user/<int:user_id>/history', methods=['GET'])
@require_auth
def user_transaction_history(user_id):
    """Get transaction history for a specific user"""
    try:
        limit = request.args.get('limit', 50, type=int)

        db: Session = SessionLocal()
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            db.close()
            return jsonify({'error': 'User not found'}), 404

        transactions = db.query(BeneficiaryTransaction).filter(
            BeneficiaryTransaction.user_id == user_id
        ).order_by(BeneficiaryTransaction.timestamp.desc()).limit(limit).all()

        db.close()

        # Calculate statistics
        total_quantity = sum(t.quantity for t in transactions)
        avg_quantity = total_quantity / len(transactions) if transactions else 0

        return jsonify({
            'user_id': user_id,
            'user_name': user.name,
            'count': len(transactions),
            'total_quantity': total_quantity,
            'avg_quantity': avg_quantity,
            'transactions': [
                {
                    'id': t.id,
                    'shop_id': t.shop_id,
                    'quantity': t.quantity,
                    'timestamp': t.timestamp.isoformat()
                }
                for t in transactions
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
