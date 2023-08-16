from rest_framework.routers import DefaultRouter
from apps.recomendation.api.viewsets import RecomendationViewset
router = DefaultRouter()
router.register(r'RecomendationViewset',RecomendationViewset,basename='RecomendationViewset')
urlpatterns = router.urls