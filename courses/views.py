from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required

from django.http import HttpResponse

from django.template.response import TemplateResponse

from accounts.models import Student, Teacher

from courses.models import Course, Exam, CourseTime
from courses.forms import *

@permission_required('courses.add_course')
def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            new_course = Course.objects.create(
                id                 = form.cleaned_data['id'],
                name               = form.cleaned_data['name'],
                college            = form.cleaned_data['college'],
                classroom          = form.cleaned_data['classroom'],
                score              = form.cleaned_data['score'],
                max_student_number = form.cleaned_data['max_student_number'],
                remark             = form.cleaned_data['remark'],
            )

            return redirect('/')
    else:
        form = AddCourseForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'courses/add_course.html', context)

@permission_required('courses.change_course')
def edit_course(request, course_id):
    if request.method == 'POST':
        form = EditCourseForm(request.POST)
        if form.is_valid():
            course = Course.objects.filter(id=course_id)
            course.update(
                name               = form.cleaned_data['name'],
                college            = form.cleaned_data['college'],
                classroom          = form.cleaned_data['classroom'],
                score              = form.cleaned_data['score'],
                max_student_number = form.cleaned_data['max_student_number'],
                remark             = form.cleaned_data['remark'],
            )

            return redirect('/')

@permission_required('courses.change_course')
def add_course_teacher(request, course_id):
    if request.method == 'POST':
        request.POST['course_id'] = course_id
        form = AddCourseTeacherForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data['teacher_id']
            course_id = form.cleaned_data['course_id']
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(id=teacher_id)
            course.teacher.add(teacher)
            return redirect('/courses/add/coursetime/'+course_id)
    return redirect('/courses/extra_info/')

@permission_required('courses.add_coursetime')
def add_coursetime(request, course_id):
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        weekday = request.POST['weekday']
        begin = request.POST['begin']
        end = request.POST['end']
        coursetime = CourseTime.objects.create(
            course=course,
            weekday=weekday,
            begin=begin,
            end=end,
        )
        return redirect('/courses/add/exam/'+course_id)

@permission_required('courses.add_exam')
def add_exam(request, course_id):
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        method = request.POST['method']
        date = request.POST['date']
        time = request.POST['time']
        exam = Exam.objects.create(
            course=course,
            method=method,
            date=date,
            time=time,
        )
        return redirect('/courses/manager/')

@permission_required('courses.delete_course')
def delete_course(request):
    if request.method == 'POST':
        form = DeleteCourseForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            course = Course.objects.get(id=id)
            course.delete()
    else:
        form = DeleteCourseForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'courses/delete.html', context)

@login_required
def pick_course(request):
    if request.method == 'POST':
        form = PickCourseForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            course_id = form.cleaned_data['course_id']
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            course.student.add(student)
            return redirect('/')
    else:
        form = PickCourseForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'courses/pick_course.html', context)

@login_required
def drop_course(request):
    if request.method == 'POST':
        form = DropCourseForm(request.POST)
        if form.is_valid():
            student_id = request.POST['student_id']
            course_id = request.POST['course_id']
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            course.student.remove(student)
            return redirect('/')
    else:
        form = DropCourseForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'courses/drop_course.html', context)

def search_course(request, search_content):
    search_by_course = Course.objects.filter(name__icontains=search_content)
    search_by_teacher = Course.objects.filter(teacher__name__icontains=search_content)
    search_by_college = Course.objects.filter(college__icontains=search_content)
    context = {
        'teacher_results': search_by_teacher,
        'course_results': search_by_course,
        'college_results': search_by_college,
    }
    return TemplateResponse(request, "courses/search_results.html", context)

@login_required
def student_view(request):
    user = request.user
    try:
        student = user.student
    except:
        redirect('/')
    WEEKDAY_ITER = {
        'Mon': 0,
        'Tue': 1,
        'Wed': 2,
        'Thu': 3,
        'Fri': 4,
        'Sat': 5,
        'Sun': 6,
    }
    picked_courses = student.course_set.all()
    class_table = [['' for j in range(7)] for i in range(14)]
    for picked_course in picked_courses:
        for course_time in picked_course.coursetime_set.all():
            class_table[course_time.begin-1][WEEKDAY_ITER[course_time.weekday]] = course_time

    context = {
        'courses': picked_courses,
        'class_table': class_table,
    }

    return TemplateResponse(request, 'courses/student.html', context)
