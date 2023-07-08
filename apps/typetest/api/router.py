from rest_framework.routers import DefaultRouter
from apps.typetest.api.viewsets import TypeTestViewSet
router = DefaultRouter()
router.register(r'TypeTestViewSet',TypeTestViewSet,basename='TypeTestViewSet')
urlpatterns = router.urls