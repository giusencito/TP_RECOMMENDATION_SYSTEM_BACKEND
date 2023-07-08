from django.db import models
from apps.base.models import BaseModel
from apps.section.models import Section
# Create your models here.
class Question(BaseModel):
    questionname = models.CharField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    class Meta:
          verbose_name = 'Question'
          verbose_name_plural = 'Questions'
    
    def __str__(self):
           
        return f'{self.id} is  called {self.questionname}'