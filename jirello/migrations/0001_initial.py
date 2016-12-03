# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('date_comment', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=128)),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'O', max_length=2, null=True, choices=[('O', 'Open'), ('R', 'Ready to develop'), ('I', 'In progress'), ('C', 'Code Review'), ('V', 'Verification'), ('D', 'Done')])),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('original_estimate', models.PositiveIntegerField()),
                ('remaining_estimate', models.PositiveIntegerField()),
                ('storypoints', models.PositiveSmallIntegerField(default=0, null=True, choices=[(2, b'1'), (3, b'2'), (4, b'3'), (5, b'5'), (6, b'8'), (7, b'13'), (8, b'21')])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=128, db_index=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name=b'email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_super', models.BooleanField(default=False)),
                ('picture', models.ImageField(upload_to=b'/profile_images', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Worklog',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='jirello.Comment')),
            ],
            bases=('jirello.comment',),
        ),
        migrations.AddField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(related_name='own', to='jirello.User'),
        ),
        migrations.AddField(
            model_name='task',
            name='sprints',
            field=models.ManyToManyField(related_name='task', to='jirello.Sprint'),
        ),
        migrations.AddField(
            model_name='task',
            name='worker',
            field=models.ForeignKey(related_name='task', to='jirello.User'),
        ),
        migrations.AddField(
            model_name='sprint',
            name='owner',
            field=models.ForeignKey(related_name='sprint', to='jirello.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(related_name='comment', to='jirello.Task'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name='comment', to='jirello.User'),
        ),
    ]
