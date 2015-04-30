# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetime',
            name='begin',
            field=models.PositiveSmallIntegerField(choices=[(1, b'\xe7\xac\xac 1 \xe8\x8a\x82'), (2, b'\xe7\xac\xac 2 \xe8\x8a\x82'), (3, b'\xe7\xac\xac 3 \xe8\x8a\x82'), (4, b'\xe7\xac\xac 4 \xe8\x8a\x82'), (5, b'\xe7\xac\xac 5 \xe8\x8a\x82'), (6, b'\xe7\xac\xac 6 \xe8\x8a\x82'), (7, b'\xe7\xac\xac 7 \xe8\x8a\x82'), (8, b'\xe7\xac\xac 8 \xe8\x8a\x82'), (9, b'\xe7\xac\xac 9 \xe8\x8a\x82'), (10, b'\xe7\xac\xac 10 \xe8\x8a\x82'), (11, b'\xe7\xac\xac 11 \xe8\x8a\x82'), (12, b'\xe7\xac\xac 12 \xe8\x8a\x82'), (13, b'\xe7\xac\xac 13 \xe8\x8a\x82'), (14, b'\xe7\xac\xac 14 \xe8\x8a\x82')]),
        ),
        migrations.AlterField(
            model_name='coursetime',
            name='end',
            field=models.PositiveSmallIntegerField(choices=[(1, b'\xe7\xac\xac 1 \xe8\x8a\x82'), (2, b'\xe7\xac\xac 2 \xe8\x8a\x82'), (3, b'\xe7\xac\xac 3 \xe8\x8a\x82'), (4, b'\xe7\xac\xac 4 \xe8\x8a\x82'), (5, b'\xe7\xac\xac 5 \xe8\x8a\x82'), (6, b'\xe7\xac\xac 6 \xe8\x8a\x82'), (7, b'\xe7\xac\xac 7 \xe8\x8a\x82'), (8, b'\xe7\xac\xac 8 \xe8\x8a\x82'), (9, b'\xe7\xac\xac 9 \xe8\x8a\x82'), (10, b'\xe7\xac\xac 10 \xe8\x8a\x82'), (11, b'\xe7\xac\xac 11 \xe8\x8a\x82'), (12, b'\xe7\xac\xac 12 \xe8\x8a\x82'), (13, b'\xe7\xac\xac 13 \xe8\x8a\x82'), (14, b'\xe7\xac\xac 14 \xe8\x8a\x82')]),
        ),
        migrations.AlterField(
            model_name='coursetime',
            name='weekday',
            field=models.CharField(max_length=3, choices=[(b'Mon', b'\xe5\x91\xa8\xe4\xb8\x80'), (b'Tue', b'\xe5\x91\xa8\xe4\xba\x8c'), (b'Wed', b'\xe5\x91\xa8\xe4\xb8\x89'), (b'Thu', b'\xe5\x91\xa8\xe5\x9b\x9b'), (b'Fri', b'\xe5\x91\xa8\xe4\xba\x94'), (b'Sat', b'\xe5\x91\xa8\xe5\x85\xad'), (b'Sun', b'\xe5\x91\xa8\xe6\x97\xa5')]),
        ),
        migrations.AlterField(
            model_name='exam',
            name='time',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
