from rest_framework.routers import DefaultRouter
from apps.option.api.viewsets import OptionViewSet
router = DefaultRouter()
router.register(r'OptionViewSet',OptionViewSet,basename='OptionViewSet')
urlpatterns = router.urls