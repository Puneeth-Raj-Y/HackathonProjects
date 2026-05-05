"""
Grievance Management Routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.db import SessionLocal
from models import Grievance, User
from utils.auth_utils import get_token_from_request, verify_access_token

grievance_bp = Blueprint('grievance', __name__)


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


@grievance_bp.route('', methods=['POST'])
@require_auth
def create_grievance():
    """
    Create a new grievance
    
    Expected JSON:
    {
        "user_id": 1,
        "description": "Did not receive full quantity last time"
    }
    """
    try:
        data = request.get_json()
        
        if 'user_id' not in data or 'description' not in data:
            return jsonify({'error': 'Missing user_id or description'}), 400

        # Users can only create grievances for themselves
        if request.user_role != 'admin' and request.user_id != data['user_id']:
            return jsonify({'error': 'Cannot create grievance for other users'}), 403

        db: Session = SessionLocal()
        
        # Verify user exists
        user = db.query(User).filter(User.id == data['user_id']).first()
        if not user:
            db.close()
            return jsonify({'error': 'User not found'}), 404

        grievance = Grievance(
            user_id=data['user_id'],
            description=data['description'],
            status='open'
        )

        db.add(grievance)
        db.commit()
        grievance_id = grievance.id
        db.close()

        return jsonify({
            'message': 'Grievance created successfully',
            'grievance_id': grievance_id,
            'status': 'open'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@grievance_bp.route('/all', methods=['GET'])
@require_auth
def get_grievances():
    """
    Get grievances
    
    Query parameters:
    - user_id: filter by user
    - status: filter by status (open, resolved, closed)
    - limit: number of records to return
    """
    try:
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status')
        limit = request.args.get('limit', 100, type=int)

        db: Session = SessionLocal()
        
        query = db.query(Grievance)

        # Users can only see their own grievances unless admin
        if request.user_role != 'admin':
            query = query.filter(Grievance.user_id == request.user_id)
        elif user_id:
            query = query.filter(Grievance.user_id == user_id)

        if status:
            query = query.filter(Grievance.status == status)

        grievances = query.order_by(
            Grievance.created_at.desc()
        ).limit(limit).all()

        db.close()

        return jsonify({
            'count': len(grievances),
            'grievances': [
                {
                    'id': g.id,
                    'user_id': g.user_id,
                    'description': g.description,
                    'status': g.status,
                    'created_at': g.created_at.isoformat(),
                    'updated_at': g.updated_at.isoformat()
                }
                for g in grievances
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@grievance_bp.route('/<int:grievance_id>', methods=['GET'])
@require_auth
def get_grievance(grievance_id):
    """Get details of a specific grievance"""
    try:
        db: Session = SessionLocal()
        
        grievance = db.query(Grievance).filter(
            Grievance.id == grievance_id
        ).first()

        if not grievance:
            db.close()
            return jsonify({'error': 'Grievance not found'}), 404

        # Users can only see their own grievances
        if request.user_role != 'admin' and request.user_id != grievance.user_id:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403

        user = db.query(User).filter(User.id == grievance.user_id).first()
        db.close()

        return jsonify({
            'grievance': {
                'id': grievance.id,
                'user_id': grievance.user_id,
                'user_name': user.name if user else 'Unknown',
                'description': grievance.description,
                'status': grievance.status,
                'created_at': grievance.created_at.isoformat(),
                'updated_at': grievance.updated_at.isoformat()
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@grievance_bp.route('/<int:grievance_id>/status', methods=['PUT'])
@require_auth
def update_grievance_status(grievance_id):
    """
    Update grievance status
    
    Expected JSON:
    {
        "status": "resolved"  // open, resolved, closed
    }
    """
    try:
        # Only admins can update grievance status
        if request.user_role != 'admin':
            return jsonify({'error': 'Only admins can update grievance status'}), 403

        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Missing status field'}), 400

        valid_statuses = ['open', 'resolved', 'closed']
        if data['status'] not in valid_statuses:
            return jsonify({
                'error': f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            }), 400

        db: Session = SessionLocal()
        
        grievance = db.query(Grievance).filter(
            Grievance.id == grievance_id
        ).first()

        if not grievance:
            db.close()
            return jsonify({'error': 'Grievance not found'}), 404

        grievance.status = data['status']
        grievance.updated_at = datetime.utcnow()

        db.commit()
        db.close()

        return jsonify({
            'message': 'Grievance status updated',
            'grievance_id': grievance_id,
            'status': data['status']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@grievance_bp.route('/statistics', methods=['GET'])
@require_auth
def get_grievance_statistics():
    """Get grievance statistics"""
    try:
        if request.user_role != 'admin':
            return jsonify({'error': 'Only admins can view statistics'}), 403

        db: Session = SessionLocal()
        
        total_grievances = db.query(Grievance).count()
        open_grievances = db.query(Grievance).filter(
            Grievance.status == 'open'
        ).count()
        resolved_grievances = db.query(Grievance).filter(
            Grievance.status == 'resolved'
        ).count()
        closed_grievances = db.query(Grievance).filter(
            Grievance.status == 'closed'
        ).count()

        db.close()

        return jsonify({
            'statistics': {
                'total': total_grievances,
                'open': open_grievances,
                'resolved': resolved_grievances,
                'closed': closed_grievances,
                'resolution_rate': round(
                    (resolved_grievances + closed_grievances) / max(total_grievances, 1) * 100, 2
                )
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
