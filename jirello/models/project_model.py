from django.db import models
from .user_model import User


class ProjectModel(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

    users = models.ManyToManyField(to=User, related_name='projects')

    class Meta:
        permissions = (
            ('view_project', 'User can watch the project'),
        )

    def __unicode__(self):
        return self.title


class ProjectModelManager(models.Manager):
    pass
