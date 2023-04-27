from rest_framework.routers import DefaultRouter
from apps.postulants.api.viewsets import PostulantViewSet
router = DefaultRouter()
router.register(r'PostulantViewSet',PostulantViewSet,basename='PostulantView')
urlpatterns = router.urls