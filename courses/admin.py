from django.contrib import admin

from .models import Course, Exam, CourseTime

admin.site.register(Course)
admin.site.register(Exam)
admin.site.register(CourseTime)
