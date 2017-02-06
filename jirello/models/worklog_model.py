from django.db import models
from datetime import timedelta


class Worklog(models.Model):
    RELATED_NAME = 'worklog'
    user = models.ForeignKey('jirello.User', related_name=RELATED_NAME)
    task = models.ForeignKey('jirello.Task', related_name=RELATED_NAME)

    time_spend = models.PositiveIntegerField(blank=True, null=True)
    comment = models.CharField(max_length=400)
    date_comment = models.DateTimeField(auto_now_add=True)

    @property
    def time_show(self):
        return str(timedelta(seconds=self.time_spend))

    def __unicode__(self):
        return '{}: {}'.format(self.user, self.comment)
