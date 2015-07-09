# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=5, verbose_name=b'Department', choices=[(b'STAT', b'STAT'), (b'WC', b'Writing Center'), (b'ATH', b'Athenaeum')])),
                ('position', models.CharField(max_length=10, verbose_name=b'Position', choices=[(b'LTA', b'LTA'), (b'RTA', b'RTA'), (b'MTA', b'MTA'), (b'CONS', b'Consultant'), (b'SERVER', b'Server'), (b'KIT', b'Kitchen'), (b'SECR', b'Security'), (b'MD', b'MD')])),
                ('status', models.CharField(max_length=10, verbose_name=b'Status', choices=[(b'RGLR', b'Regular'), (b'LEAD', b'Lead'), (b'SPV', b'Supervisor')])),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='user',
            field=models.ForeignKey(related_name='positions', to=settings.AUTH_USER_MODEL),
        ),
    ]
