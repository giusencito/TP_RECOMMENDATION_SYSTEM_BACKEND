from django.shortcuts import get_object_or_404
from apps.user.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.user.api.serializer import (UserSerializer, UserListSerializer,UpdateUserSerializer,PasswordSerializer)
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