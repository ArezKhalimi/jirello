from django.db import models
from .user_model import User
from .project_model import ProjectModel
from django.core.exceptions import ValidationError


class Sprint(models.Model):
    title = models.CharField(max_length=128, unique=True)
    date_start = models.DateField()
    date_end = models.DateField()
    is_active = models.BooleanField(blank=True)

    project = models.ForeignKey(to=ProjectModel, related_name='sprints')
    owner = models.ForeignKey(to=User, related_name='created_sprints')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Sprint, self).save(*args, **kwargs)

    def clean(self):
        if self.pk is None and self.is_active:
            raise ValidationError(
                'You can`t create active sprint. Task does not exists!')
        if self.pk is not None and self.is_active is True \
                and self.project.sprints.filter(is_active=True)\
                .exclude(pk=self.pk).exists():
            raise ValidationError('You already have active sprint!')
        if self.date_start > self.date_end:
            raise ValidationError('Wrong date range')
