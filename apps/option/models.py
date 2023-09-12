from django.db import models
from apps.base.models import BaseModel
from apps.question.models import Question
from django.core.validators import MinValueValidator
# Create your models here.
class Option(BaseModel):
    optionname= models.TextField()
    optionscore= models.IntegerField(validators=[MinValueValidator(0)])
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    class Meta:
          verbose_name = 'Option'
          verbose_name_plural = 'Optionss'
    
    def __str__(self):
           
        return f'{self.id} is  called {self.optionname} and its score is {self.optionscore}'