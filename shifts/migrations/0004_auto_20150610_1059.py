# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0003_auto_20150610_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='department',
            field=models.CharField(default=b'STAT', max_length=5, choices=[(b'STAT', b'STAT'), (b'WC', b'Writing Center'), (b'ATH', b'Athenaeum')]),
        ),
    ]
