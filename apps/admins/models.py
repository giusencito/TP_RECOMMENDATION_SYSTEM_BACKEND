from django.db import models
from apps.user.models import  User
# Create your models here.
class Admin(User):
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
    user_ptr = models.OneToOneField(User,
        on_delete=models.CASCADE,
        parent_link=True,primary_key=True,
    )
    registerDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return f'Admin {self.name} {self.last_name}'