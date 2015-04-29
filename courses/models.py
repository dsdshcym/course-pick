# encoding: utf-8

from django.db import models

from accounts.models import Student, Teacher

class Course(models.Model):
    """
    Course informations
    """
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=40)
    college = models.CharField(max_length=40)
    classroom = models.CharField(max_length=40)
    score = models.DecimalField(max_digits=3, decimal_places=1)
    max_student_number = models.IntegerField()
    remark = models.CharField(max_length=100)
    student = models.ManyToManyField(Student)
    teacher = models.ManyToManyField(Teacher)

    def __unicode__(self):
        return self.name

class Exam(models.Model):
    """
    A Course's Final Exam informations
    """
    KJ = 'KJ'
    BJ = 'BJ'
    LW = 'LW'
    EXAM_METHOD_CHOICES = (
        (KJ, '开卷'),
        (BJ, '闭卷'),
        (LW, '论文'),
    )
    course = models.OneToOneField(Course, primary_key=True)
    method = models.CharField(choices=EXAM_METHOD_CHOICES, default=BJ, max_length=10)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)

    def __unicode__(self):
        return self.course.__unicode__() + '_' + self.get_method_display()

class CourseTime(models.Model):
    """
    The time a course is schedueled
    """
    WEEKDAY_CHOICES = (
        ('Mon', '周一'),
        ('Tue', '周二'),
        ('Wed', '周三'),
        ('Thu', '周四'),
        ('Fri', '周五'),
        ('Sat', '周六'),
        ('Sun', '周日'),
    )
    COURSE_TIME_CHOICES = (
        (1, '第 1 节'),
        (2, '第 2 节'),
        (3, '第 3 节'),
        (4, '第 4 节'),
        (5, '第 5 节'),
        (6, '第 6 节'),
        (7, '第 7 节'),
        (8, '第 8 节'),
        (9, '第 9 节'),
        (10, '第 10 节'),
        (11, '第 11 节'),
        (12, '第 12 节'),
        (13, '第 13 节'),
        (14, '第 14 节'),
    )
    course = models.ForeignKey(Course)
    weekday = models.CharField(max_length=3, choices=WEEKDAY_CHOICES)
    begin = models.PositiveSmallIntegerField(choices=COURSE_TIME_CHOICES)
    end = models.PositiveSmallIntegerField(choices=COURSE_TIME_CHOICES)

    def __unicode__(self):
        return self.course.__unicode__() + '_' + self.get_weekday_display()
