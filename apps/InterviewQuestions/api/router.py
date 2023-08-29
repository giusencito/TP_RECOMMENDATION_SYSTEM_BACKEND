from rest_framework.routers import DefaultRouter
from apps.InterviewQuestions.api.viewsets import InterviewQuestionViewSets
router = DefaultRouter()
router.register(r'InterviewQuestionViewSets',InterviewQuestionViewSets,basename='InterviewQuestionViewSets')
urlpatterns = router.urls