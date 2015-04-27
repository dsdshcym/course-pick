# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
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
                ('weekday', models.CharField(max_length=2)),
                ('begin', models.PositiveSmallIntegerField()),
                ('end', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('course', models.OneToOneField(primary_key=True, serialize=False, to='courses.Course')),
                ('method', models.CharField(default=b'BJ', max_length=10, choices=[(b'KJ', b'\xe5\xbc\x80\xe5\x8d\xb7'), (b'BJ', b'\xe9\x97\xad\xe5\x8d\xb7'), (b'LW', b'\xe8\xae\xba\xe6\x96\x87')])),
                ('date', models.DateField()),
                ('time', models.TimeField()),
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
