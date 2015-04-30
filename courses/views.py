from django.shortcuts import render, redirect

from courses.models import Course, Exam, CourseTime

def add_course(request):
    if request.method == 'POST':
        Course.objects.create(
            id=request.POST['id'],
            name=request.POST['name'],
            college=request.POST['college'],
            classroom=request.POST['classroom'],
            score=request.POST['score'],
            max_student_number=request.POST['max_student_number'],
            remark=request.POST['remark'],
        )
        return redirect('/')
