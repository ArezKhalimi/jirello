# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jirello', '0004_auto_20161208_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='sprints',
            field=models.ForeignKey(related_name='projects', to='jirello.Sprint', null=True),
        ),
    ]
