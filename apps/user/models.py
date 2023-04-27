from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords
# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, username, email, name,last_name, password, is_staff,is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username, email, name,last_name, password=None, **extra_fields):
            return self._create_user(username, email, name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, name,last_name, password, True, True,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    Postulant = 1
    ADMIN = 2
    ROLE_CHOICES = (
        (Postulant, 'postulant'),
        (ADMIN, 'admin'),
       
    )
    username = models.CharField(max_length = 255, unique = True)
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 30, blank = False, null = False)
    last_name = models.CharField('Apellidos', max_length = 50, blank = False, null = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    historical = HistoricalRecords()
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    objects = UserManager()
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','name','last_name','role']

    def __str__(self):
        return f'{self.name} {self.last_name}'