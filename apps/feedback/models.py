from django.db import models
from apps.base.models import BaseModel
from apps.postulants.models import Postulant
from apps.admins.models import Admin
from apps.resultTest.models import ResultTest
# Create your models here.
class Feedback(BaseModel):
      emailsend = models.DateField(auto_now_add=True)
      postulant = models.ForeignKey(Postulant, on_delete=models.CASCADE)
      admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
      token_link= models.CharField(null=True, blank=True,max_length = 50,unique = True)
      class Meta:
              verbose_name = 'Feedback'
              verbose_name_plural = 'Feedbacks'
      def __str__(self):
           
        return f'{self.id} has {self.token_link}'