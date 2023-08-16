from rest_framework.routers import DefaultRouter
from apps.resultSection.api.viewsets import ResultSectionViewSets
router = DefaultRouter()
router.register(r'ResultSectionViewSets',ResultSectionViewSets,basename='ResultSectionViewSets')
urlpatterns = router.urls