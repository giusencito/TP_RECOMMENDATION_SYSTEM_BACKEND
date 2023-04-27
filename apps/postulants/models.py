from django.db import models
from apps.user.models import  User
# Create your models here.
class Postulant(User):
    class Meta:
        verbose_name = 'Postulant'
        verbose_name_plural = 'Postulants'
    user_ptr = models.OneToOneField(User,
        on_delete=models.CASCADE,
        parent_link=True,primary_key=True,
    )
    def __str__(self):
            return f'Postulant {self.name} {self.last_name}'
    
    