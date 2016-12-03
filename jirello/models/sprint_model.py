from django.db import models
from .user_model import User


class Sprint(models.Model):
    title = models.CharField(max_length=128, unique=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    owner = models.ForeignKey(to=User, related_name='created_sprints')

    def __unicode__(self):
        return self.username
