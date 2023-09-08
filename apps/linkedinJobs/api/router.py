from rest_framework.routers import DefaultRouter
from apps.linkedinJobs.api.viewsets import LinkedinJobsViewSets
from django.urls import path
router = DefaultRouter()
router.register(r'LinkedinJobsViewSets',LinkedinJobsViewSets,basename='LinkedinJobsViewSets')
urlpatterns=[
     path('LinkedinJobsViewSets/getLinkedinJobsByResultTestAndPostulant/<int:result_test_id>/<int:postulant_id>/', LinkedinJobsViewSets.as_view({'get': 'getLinkedinJobsByResultTestAndPostulant'}), name='linkedin-jobs-by-result-test-and-postulant'),
    path('LinkedinJobsViewSets/getLinkedinJobsByPostulantsJustOne/<int:postulant_id>/', LinkedinJobsViewSets.as_view({'get': 'getLinkedinJobsByPostulantsJustOne'}), name='linkedin-jobs-by-result-postulant-JUST-ONE'),

]
urlpatterns += router.urls