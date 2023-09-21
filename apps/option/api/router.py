from rest_framework.routers import DefaultRouter
from apps.option.api.viewsets import OptionViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'OptionViewSet',OptionViewSet,basename='OptionViewSet')
urlpatterns = [
    
    path('OptionViewSet/get_questions_with_options/<int:section_id>/', OptionViewSet.as_view({'get': 'get_questions_with_options'}), name='get_questions_with_options'),
   
]
urlpatterns += router.urls