from django.db import models
from apps.base.models import BaseModel
# Create your models here.
class  TypeTest(BaseModel):
    typename = models.CharField(max_length=30)
    class Meta:
          verbose_name = 'TypeTest'
          verbose_name_plural = 'TypeTests'
    
    def __str__(self):
           
        return f'{self.id} is  called {self.typename}'