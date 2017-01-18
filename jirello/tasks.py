from __future__ import absolute_import
from celery import shared_task
# from celery.decorators import periodic_task
# from celery.schedules import crontab
# EMAIL pack
from django.conf import settings
from django.core.mail import send_mail
from jirello.models import User

from django.db.models import Sum
# @periodic_task(
#     run_every=(crontab(
#         hour="8", minute="30", day_of_week="mon,fri")
#     )
# )

'''
u = User.objects.annotate(total_time=Sum('worklog__time_spend')).order_by('total_time')
u[0].total_time
w =Worklog.objects.values('user').annotate(sum=Sum('time_spend')
element per w 
'''


@shared_task
def send_statistic():
    users = User.objects \
        .annotate(total_time=Sum('worklog__time_spend')).order_by('total_time')
    for user in users:
        text_email = 'You spend {total_time} some text message'.format(total_time=user.total_time)
        send_mail(
            'Jirello report',
            text_email,
            settings.EMAIL_HOST_USER,
            [user.email, ],
            fail_silently=False)
    return ('hello')
