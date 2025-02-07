# registration/urls.py
from django.urls import path
from .views import RegisterAPI, LoginAPI, LogoutAPI
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
# Custom LogoutView
from .views import get_csrf_token
from . import views
from knox.views import LogoutView
urlpatterns = [
    # Use the corrected class name here
    path('register/', RegisterAPI.as_view(), name='register'),
    #   path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', LoginAPI.as_view(), name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    # path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]
