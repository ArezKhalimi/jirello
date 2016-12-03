from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# class UserProfile(models.Model):
#     user=models.OneToOneField(User)
#     picture=models.ImageField(upload_to='profile_images', blank=True)


class User(AbstractBaseUser):
    """
    Custom user class. at this
    http://blackglasses.me/2013/09/17/custom-django-user-model/
    """
    username = models.CharField(max_length=128, unique=True, db_index=True)
    email = models.EmailField('email address', unique=True)
    is_active = models.BooleanField(default=True)
    is_super = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='/profile_images', blank=True)
    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username


class Sprint(models.Model):
    title = models.CharField(max_length=128, unique=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    owner = models.ForeignKey(to=User, related_name='sprint')

    def __unicode__(self):
        return self.username


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
        #1, '1'),
        (2, '1'),
        (3, '2'),
        (4, '3'),
        (5, '5'),
        (6, '8'),
        (7, '13'),
        (8, '21'),
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

    worker = models.ForeignKey(to=User, related_name='task')
    sprints = models.ManyToManyField(to=Sprint, related_name='task')
    owner = models.ForeignKey(to=User, related_name='own')

    def __unicode__(self):
        return self.username


class Comment(models.Model):
    USER_RELATED_NAME = 'comment'
    user = models.ForeignKey(to=User, related_name=USER_RELATED_NAME)
    task = models.ForeignKey(to=Task, related_name=USER_RELATED_NAME)
    comment = models.TextField()
    date_comment = models.DateTimeField()
    


class Worklog(Comment):
	# timedelta parametr a = datetime.now() - x; a.total_seconds() / 60
    USER_RELATED_NAME = 'worklog'

