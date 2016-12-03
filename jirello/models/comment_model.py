from django.db import models
from .user_model import User
from .task_model import Task


class Comment(models.Model):
    USER_RELATED_NAME = 'comment'
    user = models.ForeignKey(to=User, related_name=USER_RELATED_NAME)
    task = models.ForeignKey(to=Task, related_name=USER_RELATED_NAME)
    comment = models.TextField()
    date_comment = models.DateTimeField()
