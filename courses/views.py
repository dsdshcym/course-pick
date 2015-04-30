from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required

from courses.models import Course, Exam, CourseTime

# @permission_required('courses.can_add_course')
def add_course(request):
    if request.method == 'POST':
        Course.objects.create(
            id                 = request.POST['id'],
            name               = request.POST['name'],
            college            = request.POST['college'],
            classroom          = request.POST['classroom'],
            score              = request.POST['score'],
            max_student_number = request.POST['max_student_number'],
            remark             = request.POST['remark'],
        )
        return redirect('/')

def delete_course(request):
    if request.method == 'POST':
        id = request.POST['id']
        course = Course.objects.get(id=id)
        course.delete()
        return redirect('/')
