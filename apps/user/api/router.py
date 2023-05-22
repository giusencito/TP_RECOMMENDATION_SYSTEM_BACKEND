from rest_framework.routers import DefaultRouter
from apps.user.api.api import UserViewSet,EmailSend,SetPassword
router = DefaultRouter()
router.register(r'UserViewSet',UserViewSet,basename='UserView')
router.register(r'EmailSend',EmailSend,basename='EmailSend')
router.register(r'SetPassword',SetPassword,basename='SetPassword')
urlpatterns = router.urls