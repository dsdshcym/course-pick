from django.contrib import admin

from accounts.models import Student, Teacher, Manager

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Manager)
