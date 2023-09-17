from rest_framework.routers import DefaultRouter
from apps.feedback.api.viewsets import FeedbackViewSets
from django.urls import path
router = DefaultRouter()
router.register(r'FeedbackViewSets',FeedbackViewSets,basename='FeedbackViewSets')
urlpatterns = [
    
    path('FeedbackViewSets/get_feedback_by_result_test/<int:result_test_id>/', FeedbackViewSets.as_view({'get': 'get_feedback_by_result_test'}), name='get_feedback_by_result_test'),
   
]
urlpatterns += router.urls