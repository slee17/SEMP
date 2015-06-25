# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationsupplement',
            name='registration_profile',
        ),
        migrations.RemoveField(
            model_name='registrationsupplement',
            name='user',
        ),
        migrations.DeleteModel(
            name='RegistrationSupplement',
        ),
    ]
