from django.shortcuts import get_object_or_404
from apps.user.models import User
from rest_framework import status,views
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import secrets
import string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from apps.user.api.serializer import (UserSerializer, UserListSerializer,UpdateUserSerializer,PasswordSerializer,ResetPasswordSerializer)
class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None
    def get_object(self, pk):
            return get_object_or_404(self.model, pk=pk)
    def get_queryset(self):
           if self.queryset is None:
               self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True).values('id', 'username', 'email', 'name')
    @action(detail=True, methods=['post'])
    def set_password(self, request,pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message': 'Contraseña actualizada correctamente'
            })
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': password_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
   
         
    
    
class EmailSend(viewsets.GenericViewSet):
    serializer_class = ResetPasswordSerializer
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            print('fff')
            user = serializer.validated_data['email']
            token = default_token_generator.make_token(user)
            user.token_password = token
            user.save()
            subject = 'Restablecer contraseña'
            from_email = 'xskulldragon@gmail.com'
            recipient_list= [user.email] 
            print(recipient_list)
            reset_password_link = f'http://localhost:4200/change-password/{token}'
            message = f'Hola {user.username},\n\nPara restablecer tu contraseña, sigue este enlace: {reset_password_link}\n\nAtentamente,\nEl equipo de tu aplicación'
            send_mail(subject, message,from_email, recipient_list,fail_silently=False)
            return Response({
                'message': 'correo enviado'
            })
        else:
            print(serializer.data)
            return Response({'message':'errror'},status= status.HTTP_400_BAD_REQUEST)

class SetPassword(viewsets.GenericViewSet):
    serializer_class = PasswordSerializer
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user =  User.objects.filter(is_active=True).get(token_password=serializer.validated_data['token'])
            user.set_password(serializer.validated_data['password'])
            user.token_password = None 
            user.save()
            return Response({
                'message': 'contraseña cambiada'
            })
        else:
                
            return Response({'message':'errror'},status= status.HTTP_400_BAD_REQUEST)
        
        

    