from django.db import models
from apps.base.models import BaseModel
from apps.postulants.models import Postulant
# Create your models here.
class ResultTest(BaseModel):
      obtainDate= models.DateField(auto_now_add=True)
      postulant =models.ForeignKey(Postulant, on_delete=models.CASCADE)

      class Meta:
              verbose_name = 'ResultTest'
              verbose_name_plural = 'ResultTests'
    
      def __str__(self):
           
        return f'{self.id} was  created {self.obtainDate}'
