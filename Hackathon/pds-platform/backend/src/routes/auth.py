"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.db import SessionLocal
from models import User, UserRole
from utils.auth_utils import hash_password, verify_password, create_access_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register new user
    
    Expected JSON:
    {
        "name": "John Doe",
        "unique_id": "AADHAAR123456",
        "password": "password123",
        "role": "beneficiary"  // admin, shop, beneficiary
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['name', 'unique_id', 'password', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate role
        try:
            role = UserRole[data['role'].upper()]
        except KeyError:
            return jsonify({'error': 'Invalid role. Must be: admin, shop, beneficiary'}), 400

        db: Session = SessionLocal()
        
        # Check if user already exists
        existing_user = db.query(User).filter(
            User.unique_id == data['unique_id']
        ).first()
        
        if existing_user:
            db.close()
            return jsonify({'error': 'User with this ID already exists'}), 409

        # Create new user
        hashed_password = hash_password(data['password'])
        new_user = User(
            name=data['name'],
            unique_id=data['unique_id'],
            password=hashed_password,
            role=role
        )

        db.add(new_user)
        db.commit()
        user_id = new_user.id
        db.close()

        # Generate token
        token = create_access_token(user_id, role.value)

        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'token': token,
            'role': role.value
        }), 201

    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    
    Expected JSON:
    {
        "unique_id": "AADHAAR123456",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if 'unique_id' not in data or 'password' not in data:
            return jsonify({'error': 'Missing unique_id or password'}), 400

        db: Session = SessionLocal()
        
        # Find user
        user = db.query(User).filter(
            User.unique_id == data['unique_id']
        ).first()

        db.close()

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Verify password
        if not verify_password(data['password'], user.password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Generate token
        token = create_access_token(user.id, user.role.value)

        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'token': token,
            'role': user.role.value,
            'name': user.name
        }), 200

    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify if token is valid"""
    try:
        from utils.auth_utils import get_token_from_request, verify_access_token
        
        token = get_token_from_request(request)
        if not token:
            return jsonify({'error': 'No token provided'}), 401

        payload = verify_access_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        return jsonify({
            'message': 'Token is valid',
            'user_id': payload['user_id'],
            'role': payload['role']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
