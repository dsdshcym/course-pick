from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required

from django.http import HttpResponse

from django.template.response import TemplateResponse

from accounts.models import Student, Teacher

from courses.models import Course, Exam, CourseTime
from courses.forms import AddCourseForm

@permission_required('courses.add_course')
def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        # print form
        if form.is_valid():
            new_course = Course.objects.create(
                id                 = request.POST['id'],
                name               = request.POST['name'],
                college            = request.POST['college'],
                classroom          = request.POST['classroom'],
                score              = request.POST['score'],
                max_student_number = request.POST['max_student_number'],
                remark             = request.POST['remark'],
            )

            # exam = request.POST['exam']
            # new_exam = Exam.objects.create(
            #     course=new_course,
            #     method=exam['method'],
            #     date=exam['date'],
            #     time=exam['time'],
            # )
            return redirect('/')

@permission_required('courses.change_course')
def add_course_teacher(request, course_id):
    if request.method == 'POST':
        teacher_id = request.POST['id']
        course = Course.objects.get(id=course_id)
        teacher = Teacher.objects.get(id=teacher_id)
        course.teacher.add(teacher)
        return redirect('/courses/add/coursetime/'+course_id)

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
        picked_courses = student.course_set.all()
        for picked_course in picked_courses:
            for picked_course_time in picked_course.coursetime_set.all():
                for course_time in course.coursetime_set.all():
                    if (course_time.weekday == picked_course_time.weekday) and (course_time.end >= picked_course_time.begin) and (picked_course_time.end >= course_time.begin):
                        return redirect('/')
        course.student.add(student)
        return redirect('/')

def drop_course(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        course_id = request.POST['course_id']
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
        course.student.remove(student)
        return redirect('/')

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
    class_table = [[None for j in range(8)] for i in range(15)]
    for picked_course in picked_courses:
        for course_time in picked_course.coursetime_set.all():
            class_table[course_time.begin-1][WEEKDAY_ITER[course_time.weekday]] = picked_course

    context = {
        'courses': picked_courses,
        'class_table': class_table,
    }

    return TemplateResponse(request, 'courses/student.html', context)
