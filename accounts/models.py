from django.db import models

from django.contrib.auth.models import User

class Student(models.Model):
    """
    Student information
    """
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20)

class Teacher(models.Model):
    """
    Teacherr information
    """
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=20)

class Manager(models.Model):
    """
    Manager information
    """
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20)
