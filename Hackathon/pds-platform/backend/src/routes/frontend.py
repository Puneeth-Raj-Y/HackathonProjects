"""
Frontend Routes - Serve HTML Templates
"""
from flask import Blueprint, render_template, redirect, url_for

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/', methods=['GET'])
def index():
    """Home page - redirect to login"""
    return redirect(url_for('frontend.login'))


@frontend_bp.route('/login', methods=['GET'])
def login():
    """Login page"""
    return render_template('login.html')


@frontend_bp.route('/register', methods=['GET'])
def register():
    """Registration page"""
    return render_template('register.html')


@frontend_bp.route('/admin', methods=['GET'])
def admin_dashboard():
    """Admin dashboard"""
    return render_template('admin_dashboard.html')


@frontend_bp.route('/shop', methods=['GET'])
def shop_dashboard():
    """Shop manager dashboard"""
    return render_template('shop_dashboard.html')


@frontend_bp.route('/beneficiary', methods=['GET'])
def beneficiary_dashboard():
    """Beneficiary portal"""
    return render_template('beneficiary_dashboard.html')
