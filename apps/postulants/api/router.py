from rest_framework.routers import DefaultRouter
from apps.postulants.api.viewsets import PostulantViewSet,ChangeNameViewSet,ChangeLastNameViewSet
router = DefaultRouter()
from django.urls import path, include
router.register(r'PostulantViewSet',PostulantViewSet,basename='PostulantView')
router.register(r'ChangeNameViewSet',ChangeNameViewSet,basename='ChangeNameViewSet')
router.register(r'ChangeLastNameViewSet',ChangeLastNameViewSet,basename='ChangeLastNameViewSet')
urlpatterns = [
    path('', include(router.urls)),

]