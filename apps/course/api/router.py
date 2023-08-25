from rest_framework.routers import DefaultRouter
from apps.course.api.viewsets import CourseViewSets
router = DefaultRouter()
router.register(r'CourseViewSets',CourseViewSets,basename='CourseViewSets')
urlpatterns = router.urls