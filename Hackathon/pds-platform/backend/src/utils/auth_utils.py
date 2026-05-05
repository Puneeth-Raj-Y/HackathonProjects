"""
Authentication utilities (JWT, Password hashing)
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
import os


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_access_token(user_id: int, user_role: str, expires_in: int = 3600) -> str:
    """
    Create JWT access token
    
    Args:
        user_id: User ID
        user_role: User role
        expires_in: Token expiration time in seconds
        
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'role': user_role,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    
    secret = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    return jwt.encode(payload, secret, algorithm='HS256')


def verify_access_token(token: str) -> dict:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Token payload if valid, None otherwise
    """
    try:
        secret = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_token_from_request(request):
    """Extract token from request header"""
    auth_header = request.headers.get('Authorization', '')
    
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    
    return None
