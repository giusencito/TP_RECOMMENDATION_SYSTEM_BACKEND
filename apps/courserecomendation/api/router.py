from rest_framework.routers import DefaultRouter
from apps.courserecomendation.api.viewsets import CourseRecomendationViewset
router = DefaultRouter()
router.register(r'CourseRecomendationViewset',CourseRecomendationViewset,basename='CourseRecomendationViewset')
urlpatterns = router.urls