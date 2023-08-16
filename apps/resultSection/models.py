from django.db import models
from apps.base.models import BaseModel
from apps.resultTest.models import ResultTest
from apps.section.models import Section
# Create your models here.
class ResultSection(BaseModel):
      developmentPercentage = models.IntegerField()
      section =models.ForeignKey(Section, on_delete=models.CASCADE)
      resultTest =models.ForeignKey(ResultTest, on_delete=models.CASCADE)
      class Meta:
              verbose_name = 'ResultSection'
              verbose_name_plural = 'ResultSections'
    
      def __str__(self):
           
        return f'{self.id} has {self.developmentPercentage}%'
