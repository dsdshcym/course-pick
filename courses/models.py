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
    score = models.DecimalField()
    max_student_number = models.IntegerField()
    remark = models.CharField(max_length=100)
    student = models.ManyToManyField(Student)
    teacher = models.ManyToManyField(Teacher)

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
    method = models.CharField(choices=EXAM_METHOD_CHOICES, default=BJ)
    date = models.DateField()
    time = models.TimeField()

class CourseTime(models.Model):
    """
    The time a course is schedueled
    """
    course = models.ForeignKey(Course, primary_key=True)
    weekday = models.CharField(max_length=2)
    begin = models.PositiveSmallIntegerField()
    end = models.PositiveSmallIntegerField()
