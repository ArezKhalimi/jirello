from django.db import models
from .sprint_model import Sprint
from .user_model import User


class ProjectModel(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

    sprints = models.ForeignKey(to=Sprint, related_name='projects', null=True)
    users = models.ManyToManyField(to=User, related_name='users')

    def __unicode__(self):
            return self.title


class ProjectModelManager(models.Manager):
    pass
