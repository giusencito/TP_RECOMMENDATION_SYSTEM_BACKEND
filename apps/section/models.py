from django.db import models
from apps.base.models import BaseModel
from apps.tests.models import Test
from django.core.validators import MinValueValidator
# Create your models here.
class Section(BaseModel):
    sectionname = models.CharField(max_length=50)
    totalscore = models.IntegerField(validators=[MinValueValidator(0)])
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    class Meta:
          verbose_name = 'Section'
          verbose_name_plural = 'Sections'
    
    def __str__(self):
           
        return f'{self.id} is  called {self.sectionname} and its score is {self.totalscore}'