# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myregistrationsupplement',
            name='registration_profile',
            field=models.OneToOneField(related_name='_supplement_myregistrationsupplement_supplement', editable=False, to='registration.RegistrationProfile', verbose_name='registration profile'),
        ),
    ]
