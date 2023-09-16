from rest_framework.routers import DefaultRouter
from apps.feedback.api.viewsets import FeedbackViewSets
router = DefaultRouter()
router.register(r'FeedbackViewSets',FeedbackViewSets,basename='FeedbackViewSets')
urlpatterns = router.urls