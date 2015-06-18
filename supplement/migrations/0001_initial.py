# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyRegistrationSupplement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=5, verbose_name=b'Department', choices=[(b'STAT', b'STAT'), (b'WC', b'Writing Center'), (b'ATH', b'Athenaeum')])),
                ('status', models.CharField(max_length=5, verbose_name=b'Status', choices=[(b'RGLR', b'Regular'), (b'LEAD', b'Lead'), (b'SPV', b'Supervisor')])),
                ('registration_profile', models.OneToOneField(related_name='_registration_supplement_myregistrationsupplement_supplement', editable=False, to='registration.RegistrationProfile', verbose_name='registration profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
