"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include,re_path
from todo import views
from todo import auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Auth endpoints (short URLs for frontend)
    re_path(r'^register/?$', auth_views.register, name='register'),
    re_path(r'^login/?$', auth_views.login, name='login'),
    
    # Auth endpoints (API prefix)
    re_path(r'^api/auth/register/?$', auth_views.register, name='auth_register'),
    re_path(r'^api/auth/login/?$', auth_views.login, name='auth_login'),
    re_path(r'^api/auth/me/?$', auth_views.get_current_user, name='auth_me'),
    re_path(r'^api/auth/refresh/?$', auth_views.refresh_token, name='auth_refresh'),
    re_path(r'^api/auth/forgot-password/?$', auth_views.forgot_password, name='auth_forgot_password'),
    re_path(r'^api/auth/reset-password/?$', auth_views.reset_password, name='auth_reset_password'),
    
    # Existing routes
    path("",views.clients,name='clients_root'),
    path("users/", views.clients, name='users'),
    re_path(r"^api/analysis/?$", views.analysis_api, name='financial_analysis_api'),
    re_path(r'^api/search/suggestions/?$', views.companies_search, name='search_companies_api'),
    re_path(r'^api/v1/compare/?$', views.compare_companies_api, name='compare_companies_api'),
    re_path(r'^api/v1/companies/?$', views.companies_list_api, name='companies_list_api'),
    re_path(r'^api/v1/dashboard/?$', views.dashboard_data_api, name='dashboard_data_api'),
    # Catch-all route for React SPA - must be last
    re_path(r'^(?!api/).*$', views.clients, name='react_spa_catchall'),
]