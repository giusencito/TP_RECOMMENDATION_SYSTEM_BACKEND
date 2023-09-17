from django.db import models
from apps.base.models import BaseModel
from apps.linkedinJobs.models import LinkedinJobs
# Create your models here.
class SelectedJob(BaseModel):
    register = models.DateField(auto_now_add=True)
    job = models.ForeignKey(LinkedinJobs, on_delete=models.CASCADE)
    
    class Meta:
              verbose_name = 'SelectedJob'
              verbose_name_plural = 'SelectedJobs'
    
    def __str__(self):
           
        return f'{self.id} was created in {self.register} for {self.job.jobName}'
