# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jirello', '0002_auto_20161207_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('boss', models.ForeignKey(related_name='projects', to=settings.AUTH_USER_MODEL)),
                ('sprints', models.ForeignKey(related_name='projects', to='jirello.Sprint')),
            ],
        ),
    ]
