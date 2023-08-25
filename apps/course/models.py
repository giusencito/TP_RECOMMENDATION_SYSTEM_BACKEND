from django.db import models
from apps.base.models import BaseModel
from apps.linkedinJobs.models import LinkedinJobs
# Create your models here.
class Course(BaseModel):
    courseName = models.CharField(max_length=100)
    courseDescription = models.TextField()
    Url = models.TextField()
    job = models.ForeignKey(LinkedinJobs, on_delete=models.CASCADE)
    class Meta:
              verbose_name = 'Course'
              verbose_name_plural = 'Courses'
    
    def __str__(self):
           
        return f'{self.courseName} {self.courseDescription}'
