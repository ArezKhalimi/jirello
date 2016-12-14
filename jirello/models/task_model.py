from django.db import models
from .user_model import User
from .sprint_model import Sprint


class Task(models.Model):
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

    worker = models.ForeignKey(to=User, related_name='tasks')
    sprints = models.ManyToManyField(to=Sprint, related_name='tasks')
    owner = models.ForeignKey(to=User, related_name='created_tasks')
    # parent = models.ForeignKey(to=Task, related_name='children')

    def __unicode__(self):
        return self.title
