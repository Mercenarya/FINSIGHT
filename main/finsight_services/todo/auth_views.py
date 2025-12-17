"""
Authentication Views for FINSIGHT
API endpoints for user authentication
"""

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from todo.services import auth_service
from todo.middleware.auth_middleware import jwt_required, jwt_required_async


@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    """
    Register a new user
    
    POST /api/auth/register
    
    Request Body:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepassword123",
        "role": "user"  // optional, defaults to "user"
    }
    
    Response (201):
    {
        "message": "User registered successfully",
        "user": {
            "id": "...",
            "username": "john_doe",
            "email": "john@example.com",
            "role": "user"
        }
    }
    """
    try:
        # Parse request body
        try:
            body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'error': 'Invalid JSON format',
                    'detail': 'Request body must be valid JSON'
                },
                status=400
            )
        
        # Extract fields
        username = body.get('username', '').strip()
        email = body.get('email', '').strip().lower()
        password = body.get('password', '')
        role = body.get('role', 'user').strip()
        phone = body.get('phone', '').strip()
        
        # Validate required fields
        if not username:
            return JsonResponse(
                {'error': 'Full name is required'},
                status=400
            )
        
        if not email:
            return JsonResponse(
                {'error': 'Email is required'},
                status=400
            )
        
        if not password:
            return JsonResponse(
                {'error': 'Password is required'},
                status=400
            )
        
        # Validate password length
        if len(password) < 6:
            return JsonResponse(
                {'error': 'Password must be at least 6 characters'},
                status=400
            )
        
        # Validate email format (basic check)
        if '@' not in email or '.' not in email:
            return JsonResponse(
                {'error': 'Invalid email format'},
                status=400
            )
        
        # Set default role if not provided
        valid_roles = ['investor', 'analyst', 'student', 'user']
        if role:
            role = role.lower()
            if role not in valid_roles:
                role = 'user'  # Default to 'user' if invalid
        else:
            role = 'user'  # Default role
        
        # Register user
        result = auth_service.register_user(
            username=username,
            email=email,
            password=password,
            role=role,
            phone=phone
        )
        
        if result['success']:
            return JsonResponse(
                {
                    'message': 'User registered successfully',
                    'user': result['user']
                },
                status=201
            )
        else:
            return JsonResponse(
                {'error': result['error']},
                status=400
            )
    
    except Exception as e:
        return JsonResponse(
            {
                'error': 'Registration failed',
                'detail': str(e)
            },
            status=500
        )


@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    """
    Authenticate user and return tokens
    
    POST /api/auth/login
    
    Request Body:
    {
        "email": "john@example.com",
        "password": "securepassword123"
    }
    
    Response (200):
    {
        "message": "Login successful",
        "access_token": "...",
        "refresh_token": "...",
        "token_type": "Bearer",
        "expires_in": 86400,
        "user": {
            "id": "...",
            "username": "john_doe",
            "email": "john@example.com",
            "role": "user"
        }
    }
    """
    try:
        # Parse request body
        try:
            body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'error': 'Invalid JSON format',
                    'detail': 'Request body must be valid JSON'
                },
                status=400
            )
        
        # Extract fields
        email = body.get('email', '').strip().lower()
        password = body.get('password', '')
        
        # Validate required fields
        if not email or not password:
            return JsonResponse(
                {'error': 'Email and password are required'},
                status=400
            )
        
        # Authenticate user
        result = auth_service.authenticate_user(
            email=email,
            password=password
        )
        
        if result['success']:
            return JsonResponse(
                {
                    'message': 'Login successful',
                    'access_token': result['access_token'],
                    'refresh_token': result['refresh_token'],
                    'token_type': result['token_type'],
                    'expires_in': result['expires_in'],
                    'user': result['user']
                },
                status=200
            )
        else:
            return JsonResponse(
                {'error': result['error']},
                status=401
            )
    
    except Exception as e:
        return JsonResponse(
            {
                'error': 'Login failed',
                'detail': str(e)
            },
            status=500
        )


@csrf_exempt
@require_http_methods(['GET'])
@jwt_required
def get_current_user(request):
    """
    Get current authenticated user info
    
    GET /api/auth/me
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response (200):
    {
        "id": "...",
        "username": "john_doe",
        "email": "john@example.com",
        "role": "user",
        "created_at": "2024-01-01T00:00:00"
    }
    """
    try:
        user_id = request.user_info['user_id']
        
        result = auth_service.get_user_by_id(user_id)
        
        if result['success']:
            return JsonResponse(result['user'], status=200)
        else:
            return JsonResponse(
                {'error': result['error']},
                status=404
            )
    
    except Exception as e:
        return JsonResponse(
            {
                'error': 'Failed to get user info',
                'detail': str(e)
            },
            status=500
        )


@csrf_exempt
@require_http_methods(['POST'])
def refresh_token(request):
    """
    Refresh access token using refresh token
    
    POST /api/auth/refresh
    
    Request Body:
    {
        "refresh_token": "..."
    }
    
    Response (200):
    {
        "access_token": "...",
        "token_type": "Bearer",
        "expires_in": 86400
    }
    """
    try:
        # Parse request body
        try:
            body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'error': 'Invalid JSON format',
                    'detail': 'Request body must be valid JSON'
                },
                status=400
            )
        
        # Extract refresh token
        refresh_token_str = body.get('refresh_token', '')
        
        if not refresh_token_str:
            return JsonResponse(
                {'error': 'Refresh token is required'},
                status=400
            )
        
        # Refresh access token
        result = auth_service.refresh_access_token(refresh_token_str)
        
        if result['success']:
            return JsonResponse(
                {
                    'access_token': result['access_token'],
                    'token_type': result['token_type'],
                    'expires_in': result['expires_in']
                },
                status=200
            )
        else:
            return JsonResponse(
                {'error': result['error']},
                status=401
            )
    
    except Exception as e:
        return JsonResponse(
            {
                'error': 'Token refresh failed',
                'detail': str(e)
            },
            status=500
        )


@csrf_exempt
@require_http_methods(['POST'])
def forgot_password(request):
    """
    Request password reset
    
    POST /api/auth/forgot-password
    
    Request Body:
    {
        "email": "john@example.com"
    }
    
    Response (200):
    {
        "message": "If the email exists, a reset link will be sent",
        "reset_token": "..."  // Only in development mode
    }
    """
    try:
        # Parse request body
        try:
            body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'error': 'Invalid JSON format',
                    'detail': 'Request body must be valid JSON'
                },
                status=400
            )
        
        email = body.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse(
                {'error': 'Email is required'},
                status=400
            )
        
        result = auth_service.request_password_reset(email)
        
        if result['success']:
            response_data = {
                'message': result['message']
            }
            # Include reset token in development
            if 'reset_token' in result:
                response_data['reset_token'] = result['reset_token']
                response_data['expires_in'] = result['expires_in']
            
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse(
                {'error': result['error']},
                status=400
            )
    
    except Exception as e:
        return JsonResponse(
            {
                'error': 'Password reset request failed',
                'detail': str(e)
            },
            status=500
        )


@csrf_exempt
@require_http_methods(['POST'])
def reset_password(request):
    """
    Reset password with reset token
    
    POST /api/auth/reset-password
    
    Request Body:
    {
        "reset_token": "...",
        "new_password": "newpassword123"
    }
    
    Response (200):
    {
        "message": "Password reset successfully"
    }
    """
    try:
        # Parse request body
        try:
            body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'error': 'Invalid JSON format',
                    'detail': 'Request body must be valid JSON'
                },
                status=400
            )
        
        reset_token = body.get('reset_token', '')
        new_password = body.get('new_password', '')
        
        if not reset_token:
            return JsonResponse(
                {'error': 'Reset token is required'},
                status=400
            )
        
        if not new_password:
            return JsonResponse(
                {'error': 'New password is required'},
                status=400
            )
        
        if len(new_password) < 6:
            return JsonResponse(
                {'error': 'Password must be at least 6 characters'},
                status=400
            )
        
        result = auth_service.reset_password(reset_token, new_password)
        
        if result['success']:
            return JsonResponse(
                {'message': result['message']},
                status=200
            )
        else:
            return JsonResponse(
                {'error': result['error']},
                status=400
            )
    
    except Exception as e:
        return JsonResponse(
            {
                'error': 'Password reset failed',
                'detail': str(e)
            },
            status=500
        )