from django.db import models


class ProjectModel(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

    users = models.ManyToManyField('jirello.User', related_name='projects')

    class Meta:
        permissions = (
            ('can_view', 'User can watch the project'),
        )

    def __unicode__(self):
        return self.title


class ProjectModelManager(models.Manager):
    pass
