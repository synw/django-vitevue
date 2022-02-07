"""
Application URLs
"""
from django.urls import path
from django.contrib.auth.decorators import login_required

from .views.auth import login_view, logout_view


urlpatterns = [
    path("auth/login/", login_view),
    path("auth/logout/", login_required(logout_view)),
]
