from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser):
    """
    Custom user class. at this
    http://blackglasses.me/2013/09/17/custom-django-user-model/
    """
    username = models.CharField(max_length=128, unique=True, db_index=True)
    email = models.EmailField('email address', unique=True)
    is_active = models.BooleanField(default=True)
    is_super = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='/profile_images', blank=True)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __unicode__(self):
        return self.username
