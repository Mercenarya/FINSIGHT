"""
Authentication Service for FINSIGHT
Handles user registration, login, JWT token management
"""

import bcrypt
import jwt
import os
from datetime import datetime, timedelta

# MongoDB connection settings
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'user')

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'django-insecure-5&kcg%3r12*odx87slg_5(^-p!+l=e+w17xp4up7%95jy-pjg5')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24
JWT_REFRESH_EXPIRATION_DAYS = 7


def get_db():
    """Get MongoDB database connection"""
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI)
    return client[MONGO_DB]


def generate_user_id() -> str:
    """
    Generate custom user ID like 'u1', 'u2', etc.
    """
    try:
        db = get_db()
        users_collection = db['user']
        
        # Get count of existing users
        count = users_collection.count_documents({})
        
        # Generate new ID
        new_id = f"u{count + 1}"
        
        # Make sure ID doesn't exist
        while users_collection.find_one({'_id': new_id}):
            count += 1
            new_id = f"u{count + 1}"
        
        return new_id
    
    except Exception:
        # Fallback to timestamp-based ID
        import time
        return f"u{int(time.time())}"


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Verify plain password against stored password.
    Supports both bcrypt hashed passwords and plain text passwords.
    """
    try:
        # Check if stored password is bcrypt hashed (starts with $2)
        if stored_password.startswith('$2'):
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                stored_password.encode('utf-8')
            )
        else:
            # Plain text password comparison (for legacy data)
            return plain_password == stored_password
    except Exception:
        return False


def generate_access_token(user_id: str, email: str, username: str = '') -> str:
    """Generate JWT access token"""
    payload = {
        'user_id': user_id,
        'email': email,
        'username': username,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def generate_refresh_token(user_id: str) -> str:
    """Generate JWT refresh token"""
    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=JWT_REFRESH_EXPIRATION_DAYS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return {'valid': True, 'payload': payload}
    except jwt.ExpiredSignatureError:
        return {'valid': False, 'error': 'Token has expired'}
    except jwt.InvalidTokenError as e:
        return {'valid': False, 'error': f'Invalid token: {str(e)}'}


def register_user(username: str, email: str, password: str, role: str = 'user', phone: str = '', hash_pwd: bool = True) -> dict:
    """
    Register a new user
    
    Args:
        username: User's full name
        email: User's email address
        password: User's password
        role: User's role (user, admin, expert)
        phone: User's phone number
        hash_pwd: Whether to hash the password (default: True)
    
    Returns:
        dict with success status and user data or error message
    """
    try:
        db = get_db()
        users_collection = db['user']
        
        # Check if email already exists
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return {
                'success': False,
                'error': 'Email already registered'
            }
        
        # Generate custom user ID
        user_id = generate_user_id()
        
        # Hash password if required
        final_password = hash_password(password) if hash_pwd else password
        
        # Create user document matching frontend form:
        # Full Name, Email, Phone Number, Password, Role
        user_doc = {
            '_id': user_id,
            'username': username,
            'email': email,
            'phone': phone,
            'password': final_password,
            'role': role
        }
        
        # Insert user
        users_collection.insert_one(user_doc)
        
        return {
            'success': True,
            'user': {
                'id': user_id,
                'username': username,
                'email': email,
                'phone': phone,
                'role': role
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }


def authenticate_user(email: str, password: str) -> dict:
    """
    Authenticate user and return tokens
    
    Args:
        email: User's email
        password: User's plain password
    
    Returns:
        dict with tokens and user data or error message
    """
    try:
        db = get_db()
        users_collection = db['user']
        
        # Find user by email
        user = users_collection.find_one({'email': email})
        if not user:
            return {
                'success': False,
                'error': 'Invalid email or password'
            }
        
        # Verify password (supports both hashed and plain text)
        if not verify_password(password, user['password']):
            return {
                'success': False,
                'error': 'Invalid email or password'
            }
        
        # Get user ID (string type)
        user_id = str(user['_id'])
        
        # Generate tokens
        access_token = generate_access_token(user_id, user['email'], user.get('username', ''))
        refresh_token = generate_refresh_token(user_id)
        
        return {
            'success': True,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': JWT_EXPIRATION_HOURS * 3600,
            'user': {
                'id': user_id,
                'username': user.get('username', ''),
                'email': user['email'],
                'phone': user.get('phone', ''),
                'role': user.get('role', 'user')
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Authentication failed: {str(e)}'
        }


def refresh_access_token(refresh_token: str) -> dict:
    """
    Generate new access token from refresh token
    
    Args:
        refresh_token: Valid refresh token
    
    Returns:
        dict with new access token or error
    """
    try:
        # Verify refresh token
        result = verify_token(refresh_token)
        if not result['valid']:
            return {
                'success': False,
                'error': result['error']
            }
        
        payload = result['payload']
        
        # Check token type
        if payload.get('type') != 'refresh':
            return {
                'success': False,
                'error': 'Invalid token type'
            }
        
        # Get user from database (using string ID)
        db = get_db()
        users_collection = db['user']
        user = users_collection.find_one({'_id': payload['user_id']})
        
        if not user:
            return {
                'success': False,
                'error': 'User not found'
            }
        
        # Generate new access token
        new_access_token = generate_access_token(
            str(user['_id']),
            user['email'],
            user.get('username', '')
        )
        
        return {
            'success': True,
            'access_token': new_access_token,
            'token_type': 'Bearer',
            'expires_in': JWT_EXPIRATION_HOURS * 3600
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Token refresh failed: {str(e)}'
        }


def get_user_by_id(user_id: str) -> dict:
    """
    Get user by ID
    
    Args:
        user_id: User's string ID (e.g., 'u1', 'u2')
    
    Returns:
        dict with user data or error
    """
    try:
        db = get_db()
        users_collection = db['user']
        
        # Find by string _id
        user = users_collection.find_one({'_id': user_id})
        if not user:
            return {
                'success': False,
                'error': 'User not found'
            }
        
        return {
            'success': True,
            'user': {
                'id': str(user['_id']),
                'username': user.get('username', ''),
                'email': user.get('email', '')
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to get user: {str(e)}'
        }


def request_password_reset(email: str) -> dict:
    """
    Generate password reset token
    
    Args:
        email: User's email address
    
    Returns:
        dict with reset token or error
    """
    try:
        db = get_db()
        users_collection = db['user']
        
        user = users_collection.find_one({'email': email})
        if not user:
            # Don't reveal if email exists
            return {
                'success': True,
                'message': 'If the email exists, a reset link will be sent'
            }
        
        # Generate reset token (valid for 1 hour)
        reset_token_payload = {
            'user_id': str(user['_id']),
            'email': email,
            'type': 'password_reset',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        reset_token = jwt.encode(reset_token_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        # In production, send this token via email
        # For now, return it directly
        return {
            'success': True,
            'message': 'Password reset token generated',
            'reset_token': reset_token,  # In production, don't return this, send via email
            'expires_in': 3600  # 1 hour
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Password reset request failed: {str(e)}'
        }


def reset_password(reset_token: str, new_password: str, hash_pwd: bool = True) -> dict:
    """
    Reset password using reset token
    
    Args:
        reset_token: Valid password reset token
        new_password: New password to set
        hash_pwd: Whether to hash the password (default: True)
    
    Returns:
        dict with success status or error
    """
    try:
        # Verify reset token
        result = verify_token(reset_token)
        if not result['valid']:
            return {
                'success': False,
                'error': result['error']
            }
        
        payload = result['payload']
        
        # Check token type
        if payload.get('type') != 'password_reset':
            return {
                'success': False,
                'error': 'Invalid token type'
            }
        
        # Hash new password if required
        final_password = hash_password(new_password) if hash_pwd else new_password
        
        # Update user password (using string ID)
        db = get_db()
        users_collection = db['user']
        
        update_result = users_collection.update_one(
            {'_id': payload['user_id']},
            {
                '$set': {
                    'password': final_password
                }
            }
        )
        
        if update_result.modified_count == 0:
            return {
                'success': False,
                'error': 'Failed to update password'
            }
        
        return {
            'success': True,
            'message': 'Password reset successfully'
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Password reset failed: {str(e)}'
        }
