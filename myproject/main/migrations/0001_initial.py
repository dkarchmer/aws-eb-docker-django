# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=60)),
                ('phone', models.CharField(max_length=50, blank=True)),
                ('message', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name=b'created_on')),
            ],
        ),
    ]
