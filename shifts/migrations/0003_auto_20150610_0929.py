# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0002_auto_20150610_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='day_of_the_week',
            field=models.CharField(default=b'Monday', max_length=2, choices=[(b'M', b'Monday'), (b'TU', b'Tuesday'), (b'W', b'Wednesday'), (b'TH', b'Thursday'), (b'F', b'Friday'), (b'SA', b'Saturday'), (b'SU', b'Sunday')]),
        ),
    ]
