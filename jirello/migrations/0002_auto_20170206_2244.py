# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jirello', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='title',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='task',
            name='kind',
            field=models.CharField(default='T', max_length=1, choices=[('E', 'Epic'), ('S', 'Story'), ('T', 'Task'), ('B', 'Bug'), ('t', 'SubTask'), ('b', 'StoryBug')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='O', max_length=1, null=True, choices=[('O', 'Open'), ('R', 'Ready to develop'), ('I', 'In progress'), ('C', 'Code Review'), ('V', 'Verification'), ('D', 'Done')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='storypoints',
            field=models.PositiveSmallIntegerField(default=1, null=True, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'5'), (5, b'8'), (6, b'13'), (7, b'21')]),
        ),
        migrations.AlterUniqueTogether(
            name='sprint',
            unique_together=set([('title', 'project')]),
        ),
    ]
