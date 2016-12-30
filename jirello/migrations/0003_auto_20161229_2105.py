# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jirello', '0002_auto_20161228_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_comment',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='date_end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='date_start',
            field=models.DateField(),
        ),
    ]
