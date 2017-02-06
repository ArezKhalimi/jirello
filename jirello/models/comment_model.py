from django.db import models


class Comment(models.Model):
    RELATED_NAME = 'comment'
    user = models.ForeignKey('jirello.User', related_name=RELATED_NAME)
    task = models.ForeignKey('jirello.Task', related_name=RELATED_NAME)
    comment = models.CharField(max_length=400)

    date_comment = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{}: {}'.format(self.user, self.comment)
