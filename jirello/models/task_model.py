from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.core.urlresolvers import reverse
from jirello.choices import STATUSES, STORYPOINTS, KIND


class Task(models.Model):
    kind = models.CharField(max_length=1, choices=KIND, default=KIND.TASK)
    status = models.CharField(max_length=1,
                              null=True,
                              choices=STATUSES,
                              default=STATUSES.OPEN)
    title = models.CharField(max_length=128)
    description = models.TextField()
    original_estimate = models.PositiveIntegerField()
    remaining_estimate = models.PositiveIntegerField()
    storypoints = models.PositiveSmallIntegerField(null=True,
                                                   choices=STORYPOINTS,
                                                   default=STORYPOINTS.ONE)

    project = models.ForeignKey('jirello.ProjectModel', related_name='tasks',)
    worker = models.ManyToManyField('jirello.User', related_name='tasks')
    sprints = models.ManyToManyField(
        'jirello.Sprint',
        related_name='tasks',
        blank=True
    )
    owner = models.ForeignKey('jirello.User', related_name='created_tasks')
    parent = models.ForeignKey(
        to='self', related_name='children', blank=True, null=True
    )

    @property
    def get_absolute_url(self):
        return reverse(
            'task-detail',
            kwargs={'projectmodel_id': self.project_id, 'task_id': self.pk}
        )

    @property
    def estimate_time(self):
        return str(timedelta(seconds=self.remaining_estimate))

    @property
    def original_time(self):
        return str(timedelta(seconds=self.original_estimate))

    def __unicode__(self):
        return '{}: {}'.format(self.kind, self.title)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Task, self).save(*args, **kwargs)

    def clean(self):
        if self.kind == 'E' and self.parent is not None:
            raise ValidationError('Epics can`t have any parent tasks!')
        if self.kind in ['S', 'T', 'B'] \
                and self.parent and self.parent.kind != 'E':
            raise ValidationError('Story must be able to Epic!')
        if self.kind in ['t', 'b'] and self.parent and self.parent.kind != 'S':
            raise ValidationError(
                'StoryBug or Subtask inherist just for Story')
