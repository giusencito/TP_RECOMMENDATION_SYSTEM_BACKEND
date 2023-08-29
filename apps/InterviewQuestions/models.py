from django.db import models
from apps.base.models import BaseModel
from apps.linkedinJobs.models import LinkedinJobs
# Create your models here.
class InterviewQuestions(BaseModel):
    question = models.TextField()
    answer = models.TextField()
    job = models.ForeignKey(LinkedinJobs, on_delete=models.CASCADE)
    class Meta:
              verbose_name = 'InterviewQuestion'
              verbose_name_plural = 'InterviewQuestions'
    
    def __str__(self):
           
        return f'{self.question} has {self.answer} as an answer'
