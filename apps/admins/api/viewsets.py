from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from apps.admins.models import Admin
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from apps.admins.api.serializer import (AdminSerializer,UpdateAdminSerializer,UpdateAdminNameSerializer,UpdateAdminLastnameSerializer,AdminListSerializer)

class ChangeNameViewSet(viewsets.GenericViewSet):
      serializer_class = UpdateAdminNameSerializer
      model =Admin
      def get_object(self, pk):
          return get_object_or_404(self.model, pk=pk)
      def update(self,request, pk=None):
          user = self.get_object(pk)
          user_serializer = UpdateAdminNameSerializer(user, data=request.data)
          if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Admin update'
            }, status=status.HTTP_200_OK)
          return Response({
            'message': 'An error has occured during the update',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ChangeLastNameViewSet(viewsets.GenericViewSet):
      serializer_class = UpdateAdminLastnameSerializer
      model =Admin
      def get_object(self, pk):
          return get_object_or_404(self.model, pk=pk)
      def update(self,request, pk=None):
          user = self.get_object(pk)
          user_serializer = UpdateAdminLastnameSerializer(user, data=request.data)
          if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Admin update'
            }, status=status.HTTP_200_OK)
          return Response({
            'message': 'An error has occured during the update',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
          
          
class AdminViewSet(viewsets.GenericViewSet):
      model = Admin
      serializer_class = AdminSerializer
      
      list_serializer_class = AdminListSerializer
      queryset = None
      def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)
      def get_queryset(self):
           if self.queryset is None:
               self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True).values('id', 'username', 'email', 'name')
           return self.queryset
      def list(self, request):
         users = self.get_queryset()
         users_serializer = self.list_serializer_class(users, many=True)
         return Response(users_serializer.data, status=status.HTTP_200_OK)
      @action(detail=True, methods=['get'])
      def findbyusername(self, request,pk=None):
        self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True).filter(username=pk)
        postulant = self.get_queryset()
        assitans_serializer = self.serializer_class(postulant, many=True)
        return Response(assitans_serializer.data, status=status.HTTP_200_OK)
      @action(detail=True, methods=['get'])
      def findbyname(self, request,pk=None):
        self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True).filter(name=pk)
        postulant = self.get_queryset()
        assitans_serializer = self.serializer_class(postulant, many=True)
        return Response(assitans_serializer.data, status=status.HTTP_200_OK)
     
     
      def create(self, request):
         
         serializer  = self.serializer_class(data=request.data)
         print(serializer)
         if serializer.is_valid():
          
            recipient_list= [request.data['email']] 
            name = request.data['name']
            last_name = request.data['last_name']
            username = request.data['username']
            password = request.data['password']
          
            message = f'Hola {name} {last_name},\n\nAqui tienes el usuario: {username} y la contraseña {password}\n \nAtentamente,\nEl equipo de admnistrador'
            print(message)
            subject = 'Nuevo Administrador'
            from_email = 'xskulldragon@gmail.com'
           
            
            send_mail(subject, message,from_email, recipient_list,fail_silently=False)
            serializer.save()
            
            return Response({
                'message': 'Admin register'
            }, status=status.HTTP_201_CREATED)
         print(serializer.errors)
         return Response({
            'message': 'An error has occured during the registration',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
      def retrieve(self, request,pk=None):
        Postulant = self.get_object(pk)
        user_serializer = self.serializer_class(Postulant)
        return Response(user_serializer.data)
      def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateAdminSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Admin update'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'An error has occured during the update',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
      def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
                return Response({
                'message': 'Admin deleted'
            })
        return Response({
            'message': 'Admin does not exist'
        }, status=status.HTTP_404_NOT_FOUND)

