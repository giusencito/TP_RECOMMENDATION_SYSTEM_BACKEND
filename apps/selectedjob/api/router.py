from rest_framework.routers import DefaultRouter
from apps.selectedjob.api.viewsets import SelectedJobViewSets,SendTestEmail
from django.urls import path
router = DefaultRouter()
router.register(r'SelectedJobViewSets',SelectedJobViewSets,basename='SelectedJobViewSets')
router.register(r'SelectedJobViewSets/SendTestEmail',SendTestEmail,basename='SendTestEmail')

urlpatterns = [
    path('SelectedJobViewSets/getSelectedJobsbyResultTest/<int:resulttest_id>/', SelectedJobViewSets.as_view({'get': 'getSelectedJobsbyLinkedinJobs'}), name='selectedjob-by-linkedinjob'),


]
urlpatterns += router.urls