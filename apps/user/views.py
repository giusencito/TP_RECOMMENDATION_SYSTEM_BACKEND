from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime
from apps.user.models import User

from apps.user.api.serializer import (
    CustomTokenObtainPairSerializer, CustomUserSerializer
)
# Create your views here.
class Login(TokenObtainPairView):
      serializer_class = CustomTokenObtainPairSerializer
      def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Login Succesful'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)