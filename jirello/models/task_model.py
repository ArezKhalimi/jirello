from django.db import models
from .user_model import User
from .sprint_model import Sprint
from django.core.exceptions import ValidationError
from datetime import timedelta


STATUSES = (
    (u'O', u'Open'),
    (u'R', u'Ready to develop'),
    (u'I', u'In progress'),
    (u'C', u'Code Review'),
    (u'V', u'Verification'),
    (u'D', u'Done'),
)

STORYPOINTS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '5'),
    (5, '8'),
    (6, '13'),
    (7, '21'),
)


KIND = (
    (u'E', u'Epic'),
    (u'S', u'Story'),
    (u'T', u'Task'),
    (u'B', u'Bug'),
    (u't', u'SubTask'),
    (u'b', u'StoryBug'),
)


class Task(models.Model):
    kind = models.CharField(max_length=2, choices=KIND, default='T')
    status = models.CharField(max_length=2,
                              null=True,
                              choices=STATUSES,
                              default='O')
    title = models.CharField(max_length=128)
    description = models.TextField()
    original_estimate = models.PositiveIntegerField()
    remaining_estimate = models.PositiveIntegerField()
    storypoints = models.PositiveSmallIntegerField(null=True,
                                                   choices=STORYPOINTS,
                                                   default=0)

    project = models.ForeignKey('jirello.ProjectModel', related_name='tasks',)
    worker = models.ManyToManyField(to=User, related_name='tasks')
    sprints = models.ManyToManyField(to=Sprint, related_name='tasks',
                                     blank=True)
    owner = models.ForeignKey(to=User, related_name='created_tasks')
    parent = models.ForeignKey(
        to='self', related_name='children', blank=True, null=True
    )

    @property
    def estimate_left(self):
        return str(timedelta(seconds=self.remaining_estimate))

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
