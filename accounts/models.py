from django.db import models

from django.contrib.auth.models import User

class Student(models.Model):
    """
    Student information
    """
    id = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User)
    name = models.CharField(max_length=20)

    user_type = 'student'

    def __unicode__(self):
        return "S: %s_%s" % (self.id, self.name)

class Teacher(models.Model):
    """
    Teacherr information
    """
    id = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User)
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=20)

    user_type = 'teacher'

    def __unicode__(self):
        return "T: %s_%s_%s" % (self.id, self.name, self.title)

class Manager(models.Model):
    """
    Manager information
    """
    id = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User)
    name = models.CharField(max_length=20)

    user_type = 'manager'

    def __unicode__(self):
        return "M: %s_%s" % (self.id, self.name)
