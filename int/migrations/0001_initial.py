# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-11 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('thread', models.IntegerField(blank=True, null=True)),
                ('country_code', models.TextField(blank=True, null=True)),
                ('country_path', models.TextField(blank=True, null=True)),
                ('main_post', models.NullBooleanField()),
            ],
            options={
                'db_table': 'post',
                'managed': False,
            },
        ),
    ]
