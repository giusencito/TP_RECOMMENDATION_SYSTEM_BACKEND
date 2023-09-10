from rest_framework.routers import DefaultRouter
from apps.selectedjob.api.viewsets import SelectedJobViewSets
router = DefaultRouter()
router.register(r'SelectedJobViewSets',SelectedJobViewSets,basename='SelectedJobViewSets')
urlpatterns = router.urls