from rest_framework.routers import DefaultRouter
from apps.tests.api.viewsets import TestViewSet
from django.urls import path
router = DefaultRouter()
router.register(r'TestViewSet',TestViewSet,basename='TestViewSet')
urlpatterns = [
    
    path('TestViewSet/excludeTestbyTypeTest/<int:pk1>/<int:pk2>/', TestViewSet.as_view({'get': 'excludeTestbyTypeTest'}), name='excludeTestbyTypeTest'),
   
]
urlpatterns += router.urls