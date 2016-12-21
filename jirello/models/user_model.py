from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class User(AbstractUser):
    """
    Custom user class. at this
    http://blackglasses.me/2013/09/17/custom-django-user-model/
    """
    picture = models.ImageField(upload_to='user_profile_images',
                                blank=True,
                                null=True)
    objects = UserManager()

    def __unicode__(self):
        return self.username
