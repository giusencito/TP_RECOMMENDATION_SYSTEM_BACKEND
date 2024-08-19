from rest_framework.routers import DefaultRouter
from apps.hybridRecomendation.views import HybridRecomendationViewset
router = DefaultRouter()
router.register(r'HybridRecomendationViewset',HybridRecomendationViewset,basename='HybridRecomendationViewset')
urlpatterns = router.urls