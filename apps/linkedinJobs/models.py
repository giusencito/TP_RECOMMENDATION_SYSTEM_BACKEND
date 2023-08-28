from django.db import models
from apps.base.models import BaseModel
from apps.resultTest.models import ResultTest
# Create your models here.
class LinkedinJobs(BaseModel):
    jobName = models.CharField(max_length=100)
    jobDescription = models.TextField()
    jobUrl = models.TextField()
    jobLocation = models.CharField(max_length=100, default=None)
    jobCompany = models.CharField(max_length=100, default=None)
    jobDate = models.CharField(max_length=100, default=None)
    posibilityPercentage = models.FloatField()
    resultTest=models.ForeignKey(ResultTest, on_delete=models.CASCADE)
    class Meta:
              verbose_name = 'LinkedinJob'
              verbose_name_plural = 'LinkedinJobs'
    
    def __str__(self):
           
        return f'{self.jobName} has a {self.posibilityPercentage}%'