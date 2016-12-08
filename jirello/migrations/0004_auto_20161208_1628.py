# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jirello', '0003_projectmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmodel',
            name='boss',
        ),
        migrations.AddField(
            model_name='projectmodel',
            name='users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
