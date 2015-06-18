# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seller', models.CharField(max_length=25)),
                ('buyer', models.CharField(max_length=25)),
                ('posted', models.DateField(auto_now_add=True)),
                ('bought', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='shift',
            name='ownership',
        ),
        migrations.AddField(
            model_name='shift',
            name='activated',
            field=models.BooleanField(default=False, verbose_name=b'Activation status'),
        ),
        migrations.AddField(
            model_name='shift',
            name='day_of_the_week',
            field=models.CharField(blank=True, max_length=2, choices=[(b'M', b'Monday'), (b'TU', b'Tuesday'), (b'W', b'Wednesday'), (b'TH', b'Thursday'), (b'F', b'Friday'), (b'SA', b'Saturday'), (b'SU', b'Sunday')]),
        ),
        migrations.AddField(
            model_name='shift',
            name='department',
            field=models.CharField(default=b'STAT', max_length=5, choices=[(b'STAT', b'STAT'), (b'WR', b'Writing Center'), (b'ATH', b'Athenaeum')]),
        ),
        migrations.AddField(
            model_name='shift',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='location',
            field=models.CharField(max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='owner',
            field=models.CharField(max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='shift',
            field=models.ForeignKey(to='shifts.Shift'),
        ),
    ]
