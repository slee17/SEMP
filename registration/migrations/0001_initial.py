# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_status', models.CharField(db_column=b'status', default=b'untreated', editable=False, choices=[(b'untreated', 'Untreated'), (b'accepted', 'Registration accepted'), (b'rejected', 'Registration rejected')], max_length=10, verbose_name='status')),
                ('activation_key', models.CharField(default=None, max_length=40, null=True, editable=False, verbose_name='activation key')),
                ('user', models.OneToOneField(related_name='registration_profile', editable=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
                'permissions': (('accept_registration', 'Can accept registration'), ('reject_registration', 'Can reject registration'), ('activate_user', 'Can activate user in admin site')),
            },
        ),
    ]
