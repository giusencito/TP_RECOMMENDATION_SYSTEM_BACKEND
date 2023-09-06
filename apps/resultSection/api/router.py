from rest_framework.routers import DefaultRouter
from apps.resultSection.api.viewsets import ResultSectionViewSets
from django.urls import path
router = DefaultRouter()
router.register(r'ResultSectionViewSets',ResultSectionViewSets,basename='ResultSectionViewSets')
urlpatterns = [
    
    path('getResultSectionbyTestAndResultTest/<int:test_id>/<int:result_test_id>/', ResultSectionViewSets.as_view({'get': 'getResultSectionbyTestAndResultTest'}), name='get_result_section_by_test_and_result_test'),
]
urlpatterns += router.urls