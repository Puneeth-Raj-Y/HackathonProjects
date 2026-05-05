"""
Stock Management Routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.db import SessionLocal
from models import Warehouse, Shop, StockTransaction, FraudAlert, Dispatch
from utils.auth_utils import get_token_from_request, verify_access_token

stock_bp = Blueprint('stock', __name__)


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


@stock_bp.route('/warehouses', methods=['GET'])
def get_warehouses():
    """Get all warehouses"""
    try:
        db: Session = SessionLocal()
        warehouses = db.query(Warehouse).all()
        db.close()

        return jsonify({
            'count': len(warehouses),
            'warehouses': [
                {
                    'id': w.id,
                    'name': w.name,
                    'location': w.location,
                    'created_at': w.created_at.isoformat()
                }
                for w in warehouses
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stock_bp.route('/add-warehouse', methods=['POST'])
@require_auth
def add_warehouse():
    """
    Add new warehouse (Admin only)
    
    Expected JSON:
    {
        "name": "Warehouse A",
        "location": "Delhi"
    }
    """
    try:
        if request.user_role != 'admin':
            return jsonify({'error': 'Only admins can add warehouses'}), 403

        data = request.get_json()
        
        if 'name' not in data or 'location' not in data:
            return jsonify({'error': 'Missing name or location'}), 400

        db: Session = SessionLocal()
        
        warehouse = Warehouse(
            name=data['name'],
            location=data['location']
        )

        db.add(warehouse)
        db.commit()
        warehouse_id = warehouse.id
        db.close()

        return jsonify({
            'message': 'Warehouse added successfully',
            'warehouse_id': warehouse_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stock_bp.route('/warehouse/<int:warehouse_id>/add-stock', methods=['POST'])
@require_auth
def add_stock(warehouse_id):
    """
    Add stock to warehouse
    
    Expected JSON:
    {
        "quantity": 1000.0,
        "notes": "Monthly supply from government"
    }
    """
    try:
        if request.user_role != 'admin':
            return jsonify({'error': 'Only admins can add stock'}), 403

        data = request.get_json()
        
        if 'quantity' not in data or float(data['quantity']) <= 0:
            return jsonify({'error': 'Missing or invalid quantity'}), 400

        db: Session = SessionLocal()
        
        # Verify warehouse exists
        warehouse = db.query(Warehouse).filter(
            Warehouse.id == warehouse_id
        ).first()
        
        if not warehouse:
            db.close()
            return jsonify({'error': 'Warehouse not found'}), 404

        quantity = float(data['quantity'])

        # Update warehouse stock
        warehouse.current_stock += quantity

        # Record stock transaction
        transaction = StockTransaction(
            warehouse_id=warehouse_id,
            quantity=quantity,
            transaction_type='inbound',
            notes=data.get('notes', 'Stock addition')
        )

        db.add(transaction)
        db.commit()
        transaction_id = transaction.id
        db.close()

        return jsonify({
            'message': 'Stock added successfully to warehouse',
            'transaction_id': transaction_id,
            'warehouse_id': warehouse_id,
            'quantity': quantity,
            'warehouse_stock': warehouse.current_stock
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stock_bp.route('/warehouse/<int:warehouse_id>/dispatch', methods=['POST'])
@require_auth
def dispatch_to_shop(warehouse_id):
    """
    Dispatch stock from warehouse to shop (Supply Chain Link)
    
    Expected JSON:
    {
        "shop_id": 1,
        "quantity": 500.0,
        "notes": "Bi-weekly dispatch"
    }
    """
    try:
        if request.user_role not in ['admin', 'shop']:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        
        required_fields = ['shop_id', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        quantity = float(data['quantity'])
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400

        db: Session = SessionLocal()
        
        # Verify warehouse exists
        warehouse = db.query(Warehouse).filter(
            Warehouse.id == warehouse_id
        ).first()
        
        if not warehouse:
            db.close()
            return jsonify({'error': 'Warehouse not found'}), 404

        # CRITICAL FIX #1: Check warehouse stock before dispatch
        if warehouse.current_stock < quantity:
            db.close()
            return jsonify({
                'error': 'Insufficient warehouse stock',
                'available': warehouse.current_stock,
                'requested': quantity,
                'shortage': quantity - warehouse.current_stock
            }), 400

        # Verify shop exists and linked to warehouse
        shop = db.query(Shop).filter(
            Shop.id == data['shop_id'],
            Shop.warehouse_id == warehouse_id
        ).first()
        
        if not shop:
            db.close()
            return jsonify({'error': 'Shop not found or not linked to warehouse'}), 404

        # CRITICAL FIX #2: Update warehouse stock
        warehouse.current_stock -= quantity

        # Update shop stock
        shop.current_stock += quantity

        # Record dispatch transaction for tracking
        transaction = StockTransaction(
            warehouse_id=warehouse_id,
            shop_id=data['shop_id'],
            quantity=quantity,
            transaction_type='outbound',
            notes='Dispatch to shop'
        )

        # CRITICAL FIX #3: Create Dispatch record for supply chain tracking
        dispatch = Dispatch(
            warehouse_id=warehouse_id,
            shop_id=data['shop_id'],
            quantity=quantity,
            status='completed',
            notes=data.get('notes', 'Warehouse dispatch')
        )

        db.add(transaction)
        db.add(dispatch)
        db.commit()
        transaction_id = transaction.id
        dispatch_id = dispatch.id

        result = {
            'message': 'Stock dispatched successfully',
            'transaction_id': transaction_id,
            'dispatch_id': dispatch_id,
            'warehouse_id': warehouse_id,
            'shop_id': data['shop_id'],
            'quantity': quantity,
            'warehouse_remaining_stock': warehouse.current_stock,
            'shop_current_stock': shop.current_stock
        }

        db.close()
        return jsonify(result), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stock_bp.route('/warehouse/<int:warehouse_id>/inventory', methods=['GET'])
@require_auth
def get_warehouse_inventory(warehouse_id):
    """
    Get warehouse inventory details including current stock and all linked shops
    """
    try:
        db: Session = SessionLocal()
        
        # Get warehouse details
        warehouse = db.query(Warehouse).filter(
            Warehouse.id == warehouse_id
        ).first()
        
        if not warehouse:
            db.close()
            return jsonify({'error': 'Warehouse not found'}), 404

        # Get all shops linked to this warehouse
        shops = db.query(Shop).filter(
            Shop.warehouse_id == warehouse_id
        ).all()

        # Get recent dispatch records
        recent_dispatches = db.query(Dispatch).filter(
            Dispatch.warehouse_id == warehouse_id
        ).order_by(Dispatch.dispatch_date.desc()).limit(10).all()

        db.close()

        return jsonify({
            'warehouse': {
                'id': warehouse.id,
                'name': warehouse.name,
                'location': warehouse.location,
                'current_stock': warehouse.current_stock,
                'created_at': warehouse.created_at.isoformat()
            },
            'linked_shops': [
                {
                    'id': shop.id,
                    'name': shop.name,
                    'location': shop.location,
                    'current_stock': shop.current_stock
                }
                for shop in shops
            ],
            'recent_dispatches': [
                {
                    'id': d.id,
                    'shop_id': d.shop_id,
                    'quantity': d.quantity,
                    'dispatch_date': d.dispatch_date.isoformat(),
                    'status': d.status
                }
                for d in recent_dispatches
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stock_bp.route('/history', methods=['GET'])
@require_auth
def stock_history():
    """Get stock transaction history"""
    try:
        warehouse_id = request.args.get('warehouse_id', type=int)
        shop_id = request.args.get('shop_id', type=int)
        limit = request.args.get('limit', 50, type=int)

        db: Session = SessionLocal()
        
        query = db.query(StockTransaction)
        
        if warehouse_id:
            query = query.filter(StockTransaction.warehouse_id == warehouse_id)
        
        if shop_id:
            query = query.filter(StockTransaction.shop_id == shop_id)

        transactions = query.order_by(
            StockTransaction.timestamp.desc()
        ).limit(limit).all()

        db.close()

        return jsonify({
            'count': len(transactions),
            'transactions': [
                {
                    'id': t.id,
                    'warehouse_id': t.warehouse_id,
                    'shop_id': t.shop_id,
                    'quantity': t.quantity,
                    'type': t.transaction_type,
                    'timestamp': t.timestamp.isoformat(),
                    'notes': t.notes
                }
                for t in transactions
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
