from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .managers import Usermanagers

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50 , verbose_name='Prenom')
    last_name = models.CharField(max_length=30 , verbose_name='Nom')
    username = models.CharField(max_length=30 , null=True, blank=True)
    profil = models.ImageField(
        upload_to='profils/',
        default='profils/default.jpg',
        storage=None,  
        blank=True
    )
    date_join = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = Usermanagers()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name' , 'last_name' , 'password']






