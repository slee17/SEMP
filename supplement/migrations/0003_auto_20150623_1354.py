# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '__first__'),
        ('supplement', '0002_auto_20150610_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationSupplement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=5, verbose_name=b'Department', choices=[(b'STAT', b'STAT'), (b'WC', b'Writing Center'), (b'ATH', b'Athenaeum')])),
                ('status', models.CharField(max_length=5, verbose_name=b'Status', choices=[(b'RGLR', b'Regular'), (b'LEAD', b'Lead'), (b'SPV', b'Supervisor')])),
                ('registration_profile', models.OneToOneField(related_name='_supplement_registrationsupplement_supplement', editable=False, to='registration.RegistrationProfile', verbose_name='registration profile')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='myregistrationsupplement',
            name='registration_profile',
        ),
        migrations.DeleteModel(
            name='MyRegistrationSupplement',
        ),
    ]
