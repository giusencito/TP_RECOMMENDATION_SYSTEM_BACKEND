from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from drf_yasg import openapi
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from apps.postulants.models import Postulant
from apps.postulants.api.serializer import (PostulantSerializer,PostulantListSerializer,UpdatePostulantSerializer,UpdatePostulantNameSerializer,UpdatePostulantLastnameSerializer)
from drf_yasg.utils import swagger_auto_schema
import coreapi



class ChangeNameViewSet(viewsets.GenericViewSet):
      serializer_class = UpdatePostulantNameSerializer
      model =Postulant
      def get_object(self, pk):
          return get_object_or_404(self.model, pk=pk)
      def update(self,request, pk=None):
          user = self.get_object(pk)
          user_serializer = UpdatePostulantNameSerializer(user, data=request.data)
          if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Postulant update'
            }, status=status.HTTP_200_OK)
          return Response({
            'message': 'An error has occured during the update',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
class ChangeLastNameViewSet(viewsets.GenericViewSet):
      serializer_class = UpdatePostulantLastnameSerializer
      model =Postulant
      def get_object(self, pk):
          return get_object_or_404(self.model, pk=pk)
      def update(self,request, pk=None):
          user = self.get_object(pk)
          user_serializer = UpdatePostulantLastnameSerializer(user, data=request.data)
          if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Postulant update'
            }, status=status.HTTP_200_OK)
          return Response({
            'message': 'An error has occured during the update',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PostulantViewSet(viewsets.GenericViewSet):
      model = Postulant
      serializer_class = PostulantSerializer
      
      list_serializer_class = PostulantListSerializer
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
      @action(detail=True, methods=['put'])
      def change_name(self, request, pk=None, name=None):
        self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True).filter(id=pk).get()
        self.queryset.name=name
        self.queryset.save()
        # Aquí puede usar los parámetros `pk` y `name` como lo desee en su vista
        return Response({'message': f'El nombre del objeto con ID {pk} ha sido cambiado a {name}.'})
      @action(detail=True, methods=['get'])
      def change_lastname(self, request, pk=None, last_name=None):
        self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True).filter(id=pk).get()
        self.queryset.last_name=last_name
        self.queryset.save()
        # Aquí puede usar los parámetros `pk` y `name` como lo desee en su vista
        return Response({'message': f'El nombre del objeto con ID {pk} ha sido cambiado a {last_name}.'})
     
      def create(self, request):
         
         serializer  = self.serializer_class(data=request.data)
         
         if serializer.is_valid():
          
            serializer.save()
            return Response({
                'message': 'Postulant register'
            }, status=status.HTTP_201_CREATED)
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
        user_serializer = UpdatePostulantSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Postulant update'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'An error has occured during the update',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
      def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
                return Response({
                'message': 'Postulant deleted'
            })
        return Response({
            'message': 'Postulant does not exist'
        }, status=status.HTTP_404_NOT_FOUND)


