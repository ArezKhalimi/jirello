from django.db import models
from datetime import timedelta
from .comment_model import Comment


class Worklog(Comment):
    # timedelta parametr a = datetime.now() - x; a.total_seconds() / 60
    RELATED_NAME = 'worklog'
    # time spend in sec
    time_spend = models.PositiveIntegerField()
    # Worklog.objecets.get(pk=1).time_representation

    @property
    def time_representation(self):
        return str(timedelta(seconds=self.time_spend))
