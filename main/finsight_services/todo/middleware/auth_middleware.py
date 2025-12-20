"""
JWT Authentication Middleware for FINSIGHT
Provides decorators and utilities for protecting API endpoints
"""

import functools
from django.http import JsonResponse
from todo.services import auth_service


def get_token_from_request(request):
    """
    Extract JWT token from request Authorization header
    
    Args:
        request: Django request object
    
    Returns:
        Token string or None
    """
    auth_header = request.headers.get('Authorization', '')
    
    if auth_header.startswith('Bearer '):
        return auth_header[7:]  # Remove 'Bearer ' prefix
    
    return None


def jwt_required(view_func):
    """
    Decorator to require JWT authentication for a view
    
    Usage:
        @jwt_required
        def my_protected_view(request):
            # request.user_info contains the decoded token payload
            user_id = request.user_info['user_id']
            ...
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = get_token_from_request(request)
        
        if not token:
            return JsonResponse(
                {
                    'error': 'Authentication required',
                    'detail': 'No token provided'
                },
                status=401
            )
        
        # Verify token
        result = auth_service.verify_token(token)
        
        if not result['valid']:
            return JsonResponse(
                {
                    'error': 'Authentication failed',
                    'detail': result['error']
                },
                status=401
            )
        
        # Check token type
        if result['payload'].get('type') != 'access':
            return JsonResponse(
                {
                    'error': 'Invalid token type',
                    'detail': 'Access token required'
                },
                status=401
            )
        
        # Attach user info to request
        request.user_info = result['payload']
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def jwt_required_async(view_func):
    """
    Async version of jwt_required decorator
    
    Usage:
        @jwt_required_async
        async def my_protected_view(request):
            user_id = request.user_info['user_id']
            ...
    """
    @functools.wraps(view_func)
    async def wrapper(request, *args, **kwargs):
        token = get_token_from_request(request)
        
        if not token:
            return JsonResponse(
                {
                    'error': 'Authentication required',
                    'detail': 'No token provided'
                },
                status=401
            )
        
        # Verify token
        result = auth_service.verify_token(token)
        
        if not result['valid']:
            return JsonResponse(
                {
                    'error': 'Authentication failed',
                    'detail': result['error']
                },
                status=401
            )
        
        # Check token type
        if result['payload'].get('type') != 'access':
            return JsonResponse(
                {
                    'error': 'Invalid token type',
                    'detail': 'Access token required'
                },
                status=401
            )
        
        # Attach user info to request
        request.user_info = result['payload']
        
        return await view_func(request, *args, **kwargs)
    
    return wrapper


def role_required(allowed_roles):
    """
    Decorator to require specific user roles
    Must be used after jwt_required decorator
    
    Usage:
        @jwt_required
        @role_required(['admin', 'moderator'])
        def admin_only_view(request):
            ...
    
    Args:
        allowed_roles: List of allowed role strings
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'user_info'):
                return JsonResponse(
                    {
                        'error': 'Authentication required',
                        'detail': 'Please use jwt_required decorator first'
                    },
                    status=401
                )
            
            user_role = request.user_info.get('role', 'user')
            
            if user_role not in allowed_roles:
                return JsonResponse(
                    {
                        'error': 'Access denied',
                        'detail': f'Role "{user_role}" is not allowed. Required: {allowed_roles}'
                    },
                    status=403
                )
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator


def role_required_async(allowed_roles):
    """
    Async version of role_required decorator
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        async def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'user_info'):
                return JsonResponse(
                    {
                        'error': 'Authentication required',
                        'detail': 'Please use jwt_required_async decorator first'
                    },
                    status=401
                )
            
            user_role = request.user_info.get('role', 'user')
            
            if user_role not in allowed_roles:
                return JsonResponse(
                    {
                        'error': 'Access denied',
                        'detail': f'Role "{user_role}" is not allowed. Required: {allowed_roles}'
                    },
                    status=403
                )
            
            return await view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator


def get_current_user(request):
    """
    Get current user info from request
    
    Args:
        request: Django request object with user_info attached
    
    Returns:
        User info dict or None
    """
    if hasattr(request, 'user_info'):
        return request.user_info
    return None