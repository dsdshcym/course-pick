# encoding: utf-8

from django import forms
from django.forms.extras.widgets import SelectDateWidget

from accounts.models import Student, Teacher

from courses.models import Course, CourseTime, Exam

def check_time_conflict(course_time, old_course_time):
    if (course_time.weekday == old_course_time.weekday)\
        and (((course_time.end >= old_course_time.begin) and (old_course_time.end >= course_time.begin))\
            or ((old_course_time.end >= course_time.begin) and (course_time.end >= old_course_time.begin))):
        return True
    return False

class AddCourseForm(forms.Form):
    id = forms.CharField(error_messages={'required': '课程号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)
    name = forms.CharField(error_messages={'required': '课程名不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    college = forms.CharField(error_messages={'required': '开课院系不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    classroom = forms.CharField(error_messages={'required': '上课教室不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    score = forms.DecimalField(error_messages={'required': '学分不能为空', }, max_digits=3, decimal_places=1)
    max_student_number = forms.IntegerField(error_messages={'required': '最大学生人数不能为空', 'min_value': '最大学生人数至少为 1 人', }, min_value=0)
    remark = forms.CharField(error_messages={'max_length': '最多为 100 个字符'}, max_length=100, required=False, widget=forms.Textarea)

    def clean_id(self):
        id = self.cleaned_data['id']
        exists = Course.objects.filter(id=id).count()
        if exists > 0:
            self.add_error('id', '该课程已添加，请添加其他课程或选择修改课程')
        return id

class EditCourseForm(forms.Form):
    name = forms.CharField(error_messages={'required': '课程名不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    college = forms.CharField(error_messages={'required': '开课院系不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    classroom = forms.CharField(error_messages={'required': '上课教室不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    score = forms.DecimalField(error_messages={'required': '学分不能为空', }, max_digits=3, decimal_places=1)
    max_student_number = forms.IntegerField(error_messages={'required': '最大学生人数不能为空', 'min_value': '最大学生人数至少为 1 人', }, min_value=0)
    remark = forms.CharField(error_messages={'max_length': '最多为 100 个字符'}, max_length=100, required=False, widget=forms.Textarea)

class PickCourseForm(forms.Form):
    student_id = forms.CharField(error_messages={'required': '学号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)
    course_id = forms.CharField(error_messages={'required': '课程号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)

    def clean_student_id(self):
        id = self.cleaned_data['student_id']
        exists = Student.objects.filter(id=id).count()
        if exists == 0:
            self.add_error('student_id', '该学生未注册，请核对')
        return id

    def clean_course_id(self):
        id = self.cleaned_data['course_id']
        exists = Course.objects.filter(id=id).count()
        if exists == 0:
            self.add_error('course_id', '该课程不存在，请核对')
        return id

    def clean(self):
        student_id = self.cleaned_data['student_id']
        course_id = self.cleaned_data['course_id']
        if not self.errors:
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            if student in course.student.all():
                self.add_error('course_id', '不能重复选课')
                return self.cleaned_data
            picked_courses = student.course_set.all()
            for picked_course in picked_courses:
                for picked_course_time in picked_course.coursetime_set.all():
                    for course_time in course.coursetime_set.all():
                        if check_time_conflict(course_time, picked_course_time):
                            self.add_error('course_id', '与已选课程时间冲突')
                            return self.cleaned_data
        return self.cleaned_data

class DropCourseForm(forms.Form):
    student_id = forms.CharField(error_messages={'required': '学号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)
    course_id = forms.CharField(error_messages={'required': '课程号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)

    def clean_student_id(self):
        id = self.cleaned_data['student_id']
        exists = Student.objects.filter(id=id).count()
        if exists == 0:
            self.add_error('student_id', '该学生未注册，请核对')
        return id

    def clean_course_id(self):
        id = self.cleaned_data['course_id']
        exists = Course.objects.filter(id=id).count()
        if exists == 0:
            self.add_error('course_id', '该课程不存在，请核对')
        return id

    def clean(self):
        student_id = self.cleaned_data['student_id']
        course_id = self.cleaned_data['course_id']
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
        if student not in course.student.all():
            self.add_error('course_id', '不能退未选的课程')
        return self.cleaned_data

class AddCourseTeacherForm(forms.Form):
    teacher_id = forms.CharField(error_messages={'required': '教师工号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)

    def clean_teacher_id(self):
        id = self.cleaned_data['teacher_id']
        exists = Teacher.objects.filter(id=id).count()
        if exists == 0:
            self.add_error('teacher_id', '该教师未注册，请核对')
        return id

class AddCourseTimeForm(forms.Form):
    course_id = forms.CharField(error_messages={'max_length': '最多为 20 个字符'}, max_length=20, required=False)
    weekday = forms.ChoiceField(choices=CourseTime.WEEKDAY_CHOICES)
    begin = forms.ChoiceField(choices=CourseTime.COURSE_TIME_CHOICES)
    end = forms.ChoiceField(choices=CourseTime.COURSE_TIME_CHOICES)

    def clean_course_id(self):
        id = self.cleaned_data['course_id']
        exists = Course.objects.filter(id=id).count()
        if exists == 0:
            self.add_error('course_id', '该课程不存在，请核对')
        return id

    def clean_begin(self):
        begin = self.cleaned_data['begin']
        return int(begin)

    def clean_end(self):
        end = self.cleaned_data['end']
        return int(end)

    def clean(self):
        course_id = self.cleaned_data['course_id']
        course = Course.objects.get(id=course_id)

        weekday = self.cleaned_data['weekday']
        begin = self.cleaned_data['begin']
        end = self.cleaned_data['end']

        new_course_time = CourseTime(
            course=course,
            weekday=weekday,
            begin=begin,
            end=end,
        )

        old_course_times = course.coursetime_set.filter(weekday=weekday)

        for old_course_time in old_course_times:
            if check_time_conflict(new_course_time, old_course_time):
                self.add_error('begin', '该时间与已有时间冲突，请核对')
                break

        return self.cleaned_data

class AddExamForm(forms.Form):
    course_id = forms.CharField(error_messages={'max_length': '最多为 20 个字符'}, max_length=20, required=False)
    method = forms.ChoiceField(choices=Exam.EXAM_METHOD_CHOICES)
    date = forms.DateField(error_messages={'required': '考试时间不能为空'}, widget=SelectDateWidget)
    time = forms.TimeField(required=False)

    def clean_course_id(self):
        id = self.cleaned_data['course_id']
        exists = Course.objects.filter(id=id).count()
        if exists == 0:
            self.add_error('该课程不存在，请核对')
        return id
