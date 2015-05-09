# encoding: utf-8

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

            return redirect('/courses/extra/'+new_course.id)
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
        else:
            form.id = course_id
            context = {
                'form': form,
            }
            return render(request,  'courses/detail.html', context)
    return redirect('/courses/detail/' + course_id)

def extra_info(request, course_id, teacher_form=AddCourseTeacherForm(), coursetime_form=AddCourseTimeForm(), exam_form=None):
    course = Course.objects.get(id=course_id)
    if exam_form is None:
        try:
            exam = course.exam
            exam_form = AddExamForm(
                {
                    'course_id': course.id,
                    'method': exam.method,
                    'date': exam.date,
                    'time': exam.time,
                }
            )
        except:
            exam_form = AddExamForm()
    context = {
        'course_id': course_id,
        'teacher_form': teacher_form,
        'coursetime_form': coursetime_form,
        'exam_form': exam_form,
    }
    return TemplateResponse(request, 'courses/extra_info.html', context)

@permission_required('courses.change_course')
def add_course_teacher(request, course_id):
    if request.method == 'POST':
        form = AddCourseTeacherForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data['teacher_id']
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(id=teacher_id)
            course.teacher.add(teacher)
            form = AddCourseTeacherForm()
            form.success = '添加教师成功'
    else:
        form = AddCourseTeacherForm()
    return extra_info(request, course_id, form)

@permission_required('courses.add_coursetime')
def add_coursetime(request, course_id):
    if request.method == 'POST':
        data = request.POST.dict()
        data['course_id'] = course_id
        form = AddCourseTimeForm(data)
        if form.is_valid():
            course = Course.objects.get(id=course_id)
            weekday = form.cleaned_data['weekday']
            begin = form.cleaned_data['begin']
            end = form.cleaned_data['end']
            coursetime = CourseTime.objects.create(
                course=course,
                weekday=weekday,
                begin=begin,
                end=end,
            )
            form = AddCourseTimeForm()
            form.success = '添加上课时间成功'
    else:
        form = AddCourseTimeForm()
    return extra_info(request, course_id, coursetime_form=form)

@permission_required('courses.add_exam')
def add_exam(request, course_id):
    if request.method == 'POST':
        data = request.POST.dict()
        data['course_id'] = course_id
        form = AddExamForm(data)
        if form.is_valid():
            course = Course.objects.get(id=course_id)
            method = form.cleaned_data['method']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            try:
                exam = Exam.objects.get(course=course)
                exam.course=course
                exam.method=method
                exam.date=date
                exam.time=time
            except:
                exam = Exam(
                    course=course,
                    method=method,
                    date=date,
                    time=time,
                )
            finally:
                exam.save()
            form.success = '修改考试信息成功'
    else:
        form = AddExamForm()
    return extra_info(request, course_id, exam_form=form)

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
        form = PickCourseForm(request.POST)
        course_id = request.POST['course_id']
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            course.student.add(student)
            form.success = '选课成功'
    try:
        student = request.user.student
        if hasattr(form, 'success'):
            return student_view(request, form.success)
        else:
            return student_view(request, form['course_id'].errors[0])
    except:
        pass
    try:
        teacher = request.user.teacher
        if hasattr(form, 'success'):
            return teacher_view(request, form.success)
        else:
            if form['student_id'].errors:
                return teacher_view(request, form['student_id'].errors[0])
            else:
                return teacher_view(request, form['course_id'].errors[0])
    except:
        pass
    try:
        manager = request.user.manager
        return detail(request, course_id, form)
    except:
        pass
    return redirect('/')

@login_required
def drop_course(request):
    if request.method == 'POST':
        form = DropCourseForm(request.POST)
        course_id = request.POST['course_id']
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            course.student.remove(student)
            form.success = '退课成功'
    try:
        student = request.user.student
        if hasattr(form, 'success'):
            return student_view(request, form.success)
        else:
            return student_view(request, form['course_id'].errors[0])
    except:
        pass
    try:
        teacher = request.user.teacher
        if hasattr(form, 'success'):
            return teacher_view(request, form.success)
        else:
            if form['student_id'].errors:
                return teacher_view(request, form['student_id'].errors[0])
            else:
                return teacher_view(request, form['course_id'].errors[0])
    except:
        pass
    try:
        manager = request.user.manager
        return detail(request, course_id, drop_course_form=form)
    except:
        pass
    return redirect('/')

def search_course(request):
    search_content = request.GET['q']
    search_by_id = Course.objects.filter(id__icontains=search_content)
    search_by_course = Course.objects.filter(name__icontains=search_content)
    search_by_teacher = Course.objects.filter(teacher__name__icontains=search_content)
    search_by_college = Course.objects.filter(college__icontains=search_content)
    context = {
        'id_results': search_by_id,
        'teacher_results': search_by_teacher,
        'course_results': search_by_course,
        'college_results': search_by_college,
    }
    return TemplateResponse(request, "courses/search_results.html", context)

@login_required
def student_view(request, message=None):
    user = request.user
    try:
        student = user.student
    except:
        return redirect('/')
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
            for i in range(course_time.begin, course_time.end):
                class_table[i][WEEKDAY_ITER[course_time.weekday]] = None

    context = {
        'courses': picked_courses,
        'class_table': class_table,
        'message': message,
    }

    return TemplateResponse(request, 'courses/student.html', context)

@login_required
def teacher_view(request, message=None):
    user = request.user

    try:
        teacher = user.teacher
    except:
        return redirect('/')

    courses = teacher.course_set.all()

    context = {
        'courses': courses,
        'message': message,
    }

    return TemplateResponse(request, 'courses/teacher.html', context)

@login_required
def manager_view(request):
    user = request.user

    try:
        manager = user.manager
    except:
        return redirect('/')

    return render(request, 'courses/manager.html')

def detail(request, course_id, pick_course_form=PickCourseForm(), drop_course_form=DropCourseForm()):
    course = Course.objects.get(id=course_id)
    form = EditCourseForm(
        {
            'name': course.name,
            'college': course.college,
            'classroom': course.classroom,
            'score': course.score,
            'max_student_number': course.max_student_number,
            'remark': course.remark,
        }
    )
    form.id = course_id
    context = {
        'form': form,
        'pick_course_form': pick_course_form,
        'drop_course_form': drop_course_form,
        'teachers': course.get_teacher_info(),
        'exam': course.get_exam_info(),
    }
    return TemplateResponse(request, 'courses/detail.html', context)

# TODO: Need permission_required
def clear_teacher(request):
    teacher_form = AddCourseTeacherForm()
    if request.method == 'POST':
        course_id = request.POST['course_id']
        course = Course.objects.get(id=course_id)
        course.teacher.clear()
        teacher_form.success = '清除教师信息成功，请添加正确的教师信息'
    return extra_info(request, course_id, teacher_form=teacher_form)

# TODO: Need permission_required
def clear_coursetime(request):
    coursetime_form = AddCourseTimeForm()
    if request.method == 'POST':
        course_id = request.POST['course_id']
        course = Course.objects.get(id=course_id)
        course.coursetime_set.all().delete()
        coursetime_form.success = '清除上课时间成功，请添加正确的上课时间'
    return extra_info(request, course_id, coursetime_form=coursetime_form)
