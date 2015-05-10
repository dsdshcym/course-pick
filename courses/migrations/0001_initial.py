# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('college', models.CharField(max_length=40)),
                ('classroom', models.CharField(max_length=40)),
                ('score', models.DecimalField(max_digits=3, decimal_places=1)),
                ('max_student_number', models.IntegerField()),
                ('remark', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.CharField(max_length=3, choices=[(b'Mon', b'\xe5\x91\xa8\xe4\xb8\x80'), (b'Tue', b'\xe5\x91\xa8\xe4\xba\x8c'), (b'Wed', b'\xe5\x91\xa8\xe4\xb8\x89'), (b'Thu', b'\xe5\x91\xa8\xe5\x9b\x9b'), (b'Fri', b'\xe5\x91\xa8\xe4\xba\x94'), (b'Sat', b'\xe5\x91\xa8\xe5\x85\xad'), (b'Sun', b'\xe5\x91\xa8\xe6\x97\xa5')])),
                ('begin', models.PositiveSmallIntegerField(choices=[(1, b'\xe7\xac\xac 1 \xe8\x8a\x82'), (2, b'\xe7\xac\xac 2 \xe8\x8a\x82'), (3, b'\xe7\xac\xac 3 \xe8\x8a\x82'), (4, b'\xe7\xac\xac 4 \xe8\x8a\x82'), (5, b'\xe7\xac\xac 5 \xe8\x8a\x82'), (6, b'\xe7\xac\xac 6 \xe8\x8a\x82'), (7, b'\xe7\xac\xac 7 \xe8\x8a\x82'), (8, b'\xe7\xac\xac 8 \xe8\x8a\x82'), (9, b'\xe7\xac\xac 9 \xe8\x8a\x82'), (10, b'\xe7\xac\xac 10 \xe8\x8a\x82'), (11, b'\xe7\xac\xac 11 \xe8\x8a\x82'), (12, b'\xe7\xac\xac 12 \xe8\x8a\x82'), (13, b'\xe7\xac\xac 13 \xe8\x8a\x82'), (14, b'\xe7\xac\xac 14 \xe8\x8a\x82')])),
                ('end', models.PositiveSmallIntegerField(choices=[(1, b'\xe7\xac\xac 1 \xe8\x8a\x82'), (2, b'\xe7\xac\xac 2 \xe8\x8a\x82'), (3, b'\xe7\xac\xac 3 \xe8\x8a\x82'), (4, b'\xe7\xac\xac 4 \xe8\x8a\x82'), (5, b'\xe7\xac\xac 5 \xe8\x8a\x82'), (6, b'\xe7\xac\xac 6 \xe8\x8a\x82'), (7, b'\xe7\xac\xac 7 \xe8\x8a\x82'), (8, b'\xe7\xac\xac 8 \xe8\x8a\x82'), (9, b'\xe7\xac\xac 9 \xe8\x8a\x82'), (10, b'\xe7\xac\xac 10 \xe8\x8a\x82'), (11, b'\xe7\xac\xac 11 \xe8\x8a\x82'), (12, b'\xe7\xac\xac 12 \xe8\x8a\x82'), (13, b'\xe7\xac\xac 13 \xe8\x8a\x82'), (14, b'\xe7\xac\xac 14 \xe8\x8a\x82')])),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('course', models.OneToOneField(primary_key=True, serialize=False, to='courses.Course')),
                ('method', models.CharField(default=b'BJ', max_length=10, choices=[(b'KJ', b'\xe5\xbc\x80\xe5\x8d\xb7'), (b'BJ', b'\xe9\x97\xad\xe5\x8d\xb7'), (b'LW', b'\xe8\xae\xba\xe6\x96\x87')])),
                ('date', models.DateField()),
                ('time', models.TimeField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='coursetime',
            name='course',
            field=models.ForeignKey(to='courses.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(to='accounts.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(to='accounts.Teacher'),
        ),
    ]
