from rest_framework.routers import DefaultRouter
from apps.admins.api.viewsets import AdminViewSet,ChangeNameViewSet,ChangeLastNameViewSet
router = DefaultRouter()
from django.urls import path, include
router.register(r'AdminViewSet',AdminViewSet,basename='AdminViewSet')
router.register(r'ChangeNameViewSet',ChangeNameViewSet,basename='ChangeNameViewSet')
router.register(r'ChangeLastNameViewSet',ChangeLastNameViewSet,basename='ChangeLastNameViewSet')
urlpatterns = [
    path('', include(router.urls)),

]