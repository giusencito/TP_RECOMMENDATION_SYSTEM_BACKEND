from rest_framework.routers import DefaultRouter
from apps.section.api.viewsets import SectionViewSet
router = DefaultRouter()
router.register(r'SectionViewSet',SectionViewSet,basename='SectionViewSet')
urlpatterns = router.urls