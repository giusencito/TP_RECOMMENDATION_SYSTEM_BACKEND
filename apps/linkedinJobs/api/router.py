from rest_framework.routers import DefaultRouter
from apps.linkedinJobs.api.viewsets import LinkedinJobsViewSets
router = DefaultRouter()
router.register(r'LinkedinJobsViewSets',LinkedinJobsViewSets,basename='LinkedinJobsViewSets')
urlpatterns = router.urls