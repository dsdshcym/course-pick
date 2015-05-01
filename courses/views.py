from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required

from accounts.models import Student, Teacher

from courses.models import Course, Exam, CourseTime

# @permission_required('courses.can_add_course')
def add_course(request):
    if request.method == 'POST':
        new_course = Course.objects.create(
            id                 = request.POST['id'],
            name               = request.POST['name'],
            college            = request.POST['college'],
            classroom          = request.POST['classroom'],
            score              = request.POST['score'],
            max_student_number = request.POST['max_student_number'],
            remark             = request.POST['remark'],
        )

        teacher_list = request.POST['teacher']
        for teacher in teacher_list:
            new_course.teacher.add(teacher)

        time_list = request.POST['time']
        for time_info in time_list:
            new_time = CourseTime.objects.create(
                course=new_course,
                weekday=time_info['weekday'],
                begin=time_info['begin'],
                end=time_info['end'],
            )

        exam = request.POST['exam']
        new_exam = Exam.objects.create(
            course=new_course,
            method=exam['method'],
            date=exam['date'],
            time=exam['time'],
        )
        return redirect('/')

def delete_course(request):
    if request.method == 'POST':
        id = request.POST['id']
        course = Course.objects.get(id=id)
        course.delete()
        return redirect('/')

@login_required
def pick_course(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        course_id = request.POST['course_id']
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
        course.student.add(student)
        return redirect('/')
