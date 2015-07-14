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
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_of_the_week', models.CharField(blank=True, max_length=2, null=True, choices=[(b'M', b'Monday'), (b'TU', b'Tuesday'), (b'W', b'Wednesday'), (b'TH', b'Thursday'), (b'F', b'Friday'), (b'SA', b'Saturday'), (b'SU', b'Sunday')])),
                ('location', models.CharField(default=b'Unspecified', max_length=25, choices=[(b'POPPA', b'Poppa'), (b'SOUTH', b'South'), (b'RYAL', b'Ryal')])),
                ('department', models.CharField(default=b'STAT', max_length=5, choices=[(b'STAT', b'STAT'), (b'WC', b'Writing Center'), (b'ATH', b'Athenaeum')])),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('start_time', models.TimeField(default=b'12:00:00')),
                ('end_time', models.TimeField(default=b'14:00:00')),
                ('hours', models.DurationField(editable=False)),
                ('activated', models.BooleanField(default=False, verbose_name=b'Activate')),
                ('on_sale', models.BooleanField(default=False, verbose_name=b'On sale', editable=False)),
                ('owner', models.ForeignKey(related_name='shifts', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
