from django.db import models
from apps.base.models import BaseModel
from apps.typetest.models       import TypeTest
# Create your models here.
class Test(BaseModel):
    testname = models.CharField(max_length=30)
    testdescription = models.TextField()
    typetest = models.ForeignKey(TypeTest, on_delete=models.CASCADE)
    class Meta:
          verbose_name = 'Test'
          verbose_name_plural = 'Tests'
    
    def __str__(self):
           
        return f'{self.id} is  called {self.testname}'