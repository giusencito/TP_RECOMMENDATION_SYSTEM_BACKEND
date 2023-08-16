from rest_framework.routers import DefaultRouter
from apps.resultTest.api.viewsets import ResultTestViewSets
router = DefaultRouter()
router.register(r'ResultTestViewSets',ResultTestViewSets,basename='ResultTestViewSets')
urlpatterns = router.urls