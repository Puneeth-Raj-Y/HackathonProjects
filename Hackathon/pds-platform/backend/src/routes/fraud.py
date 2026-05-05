"""
Fraud Detection and Alerts Routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.db import SessionLocal
from models import FraudAlert, BeneficiaryTransaction, StockTransaction, User
from utils.auth_utils import get_token_from_request, verify_access_token

fraud_bp = Blueprint('fraud', __name__)


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


@fraud_bp.route('/alerts', methods=['GET'])
@require_auth
def get_fraud_alerts():
    """
    Get fraud alerts
    
    Query parameters:
    - limit: number of alerts to return (default: 50)
    - risk_score_min: minimum risk score (0-1)
    - days: look back period in days (default: 7)
    - is_anomaly: filter by anomaly flag (1 or 0)
    """
    try:
        # Admin only
        if request.user_role != 'admin':
            return jsonify({'error': 'Only admins can view fraud alerts'}), 403

        limit = request.args.get('limit', 50, type=int)
        risk_score_min = request.args.get('risk_score_min', 0.5, type=float)
        days = request.args.get('days', 7, type=int)
        is_anomaly = request.args.get('is_anomaly', type=int)

        db: Session = SessionLocal()
        
        # Date filter
        date_cutoff = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(FraudAlert).filter(
            FraudAlert.created_at >= date_cutoff,
            FraudAlert.risk_score >= risk_score_min
        )

        if is_anomaly is not None:
            query = query.filter(FraudAlert.is_anomaly == is_anomaly)

        alerts = query.order_by(
            FraudAlert.created_at.desc()
        ).limit(limit).all()

        db.close()

        return jsonify({
            'count': len(alerts),
            'filters': {
                'limit': limit,
                'risk_score_min': risk_score_min,
                'days': days,
                'is_anomaly': is_anomaly
            },
            'alerts': [
                {
                    'id': a.id,
                    'transaction_id': a.stock_transaction_id or a.beneficiary_transaction_id,
                    'transaction_type': 'beneficiary' if a.beneficiary_transaction_id else 'stock',
                    'reason': a.reason,
                    'risk_score': a.risk_score,
                    'is_anomaly': bool(a.is_anomaly),
                    'created_at': a.created_at.isoformat()
                }
                for a in alerts
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@fraud_bp.route('/alerts/<int:alert_id>', methods=['GET'])
@require_auth
def get_fraud_alert_detail(alert_id):
    """Get detailed information about a specific fraud alert"""
    try:
        if request.user_role != 'admin':
            return jsonify({'error': 'Only admins can view fraud alerts'}), 403

        db: Session = SessionLocal()
        
        alert = db.query(FraudAlert).filter(FraudAlert.id == alert_id).first()

        if not alert:
            db.close()
            return jsonify({'error': 'Alert not found'}), 404

        # Get transaction details
        if alert.beneficiary_transaction_id:
            txn = db.query(BeneficiaryTransaction).filter(
                BeneficiaryTransaction.id == alert.beneficiary_transaction_id
            ).first()
            user = db.query(User).filter(User.id == txn.user_id).first()
            
            transaction_details = {
                'type': 'beneficiary',
                'user_id': txn.user_id,
                'user_name': user.name if user else 'Unknown',
                'shop_id': txn.shop_id,
                'quantity': txn.quantity,
                'timestamp': txn.timestamp.isoformat()
            }
        else:
            txn = db.query(StockTransaction).filter(
                StockTransaction.id == alert.stock_transaction_id
            ).first()
            
            transaction_details = {
                'type': 'stock',
                'warehouse_id': txn.warehouse_id,
                'shop_id': txn.shop_id,
                'quantity': txn.quantity,
                'transaction_type': txn.transaction_type,
                'timestamp': txn.timestamp.isoformat()
            }

        db.close()

        return jsonify({
            'alert': {
                'id': alert.id,
                'reason': alert.reason,
                'risk_score': alert.risk_score,
                'is_anomaly': bool(alert.is_anomaly),
                'created_at': alert.created_at.isoformat()
            },
            'transaction': transaction_details
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@fraud_bp.route('/statistics', methods=['GET'])
@require_auth
def get_fraud_statistics():
    """Get fraud detection statistics"""
    try:
        if request.user_role != 'admin':
            return jsonify({'error': 'Only admins can view statistics'}), 403

        days = request.args.get('days', 30, type=int)
        db: Session = SessionLocal()
        
        date_cutoff = datetime.utcnow() - timedelta(days=days)
        
        # Total alerts
        total_alerts = db.query(FraudAlert).filter(
            FraudAlert.created_at >= date_cutoff
        ).count()

        # High-risk alerts (risk_score > 0.7)
        high_risk_alerts = db.query(FraudAlert).filter(
            FraudAlert.created_at >= date_cutoff,
            FraudAlert.risk_score > 0.7
        ).count()

        # Anomaly detected
        anomalies = db.query(FraudAlert).filter(
            FraudAlert.created_at >= date_cutoff,
            FraudAlert.is_anomaly == 1
        ).count()

        # Average risk score
        avg_risk = db.query(FraudAlert).filter(
            FraudAlert.created_at >= date_cutoff
        ).with_entities(
            db.func.avg(FraudAlert.risk_score)
        ).scalar() or 0.0

        # Alerts by type
        beneficiary_alerts = db.query(FraudAlert).filter(
            FraudAlert.created_at >= date_cutoff,
            FraudAlert.beneficiary_transaction_id != None
        ).count()

        stock_alerts = db.query(FraudAlert).filter(
            FraudAlert.created_at >= date_cutoff,
            FraudAlert.stock_transaction_id != None
        ).count()

        db.close()

        return jsonify({
            'period_days': days,
            'statistics': {
                'total_alerts': total_alerts,
                'high_risk_alerts': high_risk_alerts,
                'anomalies_detected': anomalies,
                'average_risk_score': round(float(avg_risk), 3),
                'beneficiary_alerts': beneficiary_alerts,
                'stock_alerts': stock_alerts
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
