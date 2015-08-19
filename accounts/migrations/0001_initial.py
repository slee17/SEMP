# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last_name')),
                ('position', models.CharField(max_length=10, verbose_name='Position', choices=[(b'LTA', b'LTA'), (b'RTA', b'RTA'), (b'MTA', b'MTA'), (b'CONS', b'Consultant'), (b'SERVER', b'Server'), (b'KIT', b'Kitchen'), (b'SECR', b'Security'), (b'MD', b'MD')])),
                ('status', models.CharField(max_length=10, verbose_name=b'Status', choices=[(b'RGLR', b'Regular'), (b'LEAD', b'Lead'), (b'SPV', b'Supervisor')])),
                ('is_staff', models.BooleanField()),
            ],
            options={
                'db_table': 'auth_user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
