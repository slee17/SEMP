# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('supplement', '0003_auto_20150623_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationsupplement',
            name='user',
            field=models.OneToOneField(related_name='supplement', to=settings.AUTH_USER_MODEL),
        ),
    ]
