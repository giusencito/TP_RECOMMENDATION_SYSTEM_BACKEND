from rest_framework.routers import DefaultRouter
from apps.question.api.viewsets import QuestionViewSet
router = DefaultRouter()
router.register(r'QuestionViewSet',QuestionViewSet,basename='QuestionViewSet')
urlpatterns = router.urls