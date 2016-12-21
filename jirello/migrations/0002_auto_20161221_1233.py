# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jirello', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectmodel',
            options={'permissions': (('view_project', 'User can watch the project'),)},
        ),
    ]
