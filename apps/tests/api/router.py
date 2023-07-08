from rest_framework.routers import DefaultRouter
from apps.tests.api.viewsets import TestViewSet
router = DefaultRouter()
router.register(r'TestViewSet',TestViewSet,basename='TestViewSet')
urlpatterns = router.urls