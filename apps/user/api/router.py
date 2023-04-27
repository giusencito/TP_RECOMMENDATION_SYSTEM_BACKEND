from rest_framework.routers import DefaultRouter
from apps.user.api.api import UserViewSet
router = DefaultRouter()
router.register(r'UserViewSet',UserViewSet,basename='UserView')
urlpatterns = router.urls