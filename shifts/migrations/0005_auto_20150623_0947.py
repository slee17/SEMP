# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0004_auto_20150610_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('shift_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shifts.Shift')),
                ('seller', models.CharField(max_length=25)),
                ('buyer', models.CharField(max_length=25)),
                ('posted', models.DateField(auto_now_add=True)),
                ('bought', models.DateField(auto_now_add=True)),
            ],
            bases=('shifts.shift',),
        ),
        migrations.RemoveField(
            model_name='sales',
            name='shift',
        ),
        migrations.AlterField(
            model_name='shift',
            name='activated',
            field=models.BooleanField(default=False, verbose_name=b'Activate'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='location',
            field=models.CharField(default=b'Unspecified', max_length=25),
        ),
        migrations.AlterField(
            model_name='shift',
            name='owner',
            field=models.CharField(default=b'None', max_length=25),
        ),
        migrations.AlterField(
            model_name='shift',
            name='time',
            field=models.TimeField(),
        ),
        migrations.DeleteModel(
            name='Sales',
        ),
        migrations.AddField(
            model_name='sale',
            name='shift',
            field=models.ForeignKey(related_name='shift_sale', to='shifts.Shift'),
        ),
    ]
