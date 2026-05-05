"""
Flask Application Factory and Configuration
"""
import os
from flask import Flask
from flask_cors import CORS
from datetime import timedelta


def create_app():
    """Create and configure Flask application"""
    
    # Configure template and static folders
    # From app.py location (backend/src/config/app.py):
    # - Go up 4 levels to get to pds-platform root
    # Then access frontend/templates and frontend/static
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    template_dir = os.path.join(base_dir, 'frontend', 'templates')
    static_dir = os.path.join(base_dir, 'frontend', 'static')
    
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
        static_url_path='/static'
    )

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'sqlite:///pds_platform.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize database
    from database.db import init_db
    init_db()

    # Register blueprints
    from routes.auth import auth_bp
    from routes.stock import stock_bp
    from routes.transactions import transactions_bp
    from routes.fraud import fraud_bp
    from routes.grievance import grievance_bp
    from routes.frontend import frontend_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(stock_bp, url_prefix='/api/stock')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(fraud_bp, url_prefix='/api/fraud')
    app.register_blueprint(grievance_bp, url_prefix='/api/grievance')
    app.register_blueprint(frontend_bp)  # Frontend routes at root

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'PDS Platform API is running'}, 200

    return app
