# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplement', '0005_registrationsupplement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationsupplement',
            name='user',
        ),
    ]
