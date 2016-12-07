# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('picture', models.ImageField(upload_to=b'/profile_images', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
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
                ('is_active', models.BooleanField()),
                ('owner', models.ForeignKey(related_name='created_sprints', to=settings.AUTH_USER_MODEL)),
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
                ('storypoints', models.PositiveSmallIntegerField(default=0, null=True, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'5'), (5, b'8'), (6, b'13'), (7, b'21')])),
                ('owner', models.ForeignKey(related_name='created_tasks', to=settings.AUTH_USER_MODEL)),
                ('sprints', models.ManyToManyField(related_name='tasks', to='jirello.Sprint')),
                ('worker', models.ForeignKey(related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Worklog',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='jirello.Comment')),
                ('time_spend', models.PositiveIntegerField()),
            ],
            bases=('jirello.comment',),
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(related_name='comment', to='jirello.Task'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name='comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
