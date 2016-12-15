# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jirello', '0004_user_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='worker',
        ),
        migrations.AddField(
            model_name='task',
            name='worker',
            field=models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
