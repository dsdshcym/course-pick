# encoding: utf-8

from django import forms

from accounts.models import Student, Teacher

from courses.models import Course

class AddCourseForm(forms.Form):
    id = forms.CharField(error_messages={'required': '课程号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)
    name = forms.CharField(error_messages={'required': '课程名不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    college = forms.CharField(error_messages={'required': '开课院系不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    classroom = forms.CharField(error_messages={'required': '上课教室不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    score = forms.DecimalField(error_messages={'required': '学分不能为空', }, max_digits=3, decimal_places=1)
    max_student_number = forms.IntegerField(error_messages={'required': '最大学生人数不能为空', 'min_value': '最大学生人数至少为 1 人', }, min_value=0)
    remark = forms.CharField(error_messages={'max_length': '最多为 100 个字符'}, max_length=100, required=False)

    def clean_id(self):
        id = self.cleaned_data['id']
        exists = Course.objects.filter(id=id).count()
        if exists > 0:
            raise forms.ValidationError('该课程已添加，请添加其他课程或选择修改课程')
        return id

class EditCourseForm(forms.Form):
    name = forms.CharField(error_messages={'required': '课程名不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    college = forms.CharField(error_messages={'required': '开课院系不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    classroom = forms.CharField(error_messages={'required': '上课教室不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)
    score = forms.DecimalField(error_messages={'required': '学分不能为空', }, max_digits=3, decimal_places=1)
    max_student_number = forms.IntegerField(error_messages={'required': '最大学生人数不能为空', 'min_value': '最大学生人数至少为 1 人', }, min_value=0)
    remark = forms.CharField(error_messages={'max_length': '最多为 100 个字符'}, max_length=100, required=False)

class DeleteCourseForm(forms.Form):
    id = forms.CharField(error_messages={'required': '课程号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)
    name = forms.CharField(error_messages={'required': '课程名不能为空', 'max_length': '最多为 40 个字符'}, max_length=40)

    def clean(self):
        id = self.cleaned_data['id']
        name = self.cleaned_data['name']
        exists = Course.objects.filter(id=id, name=name).count()
        if exists == 0:
            raise forms.ValidationError('该课程不存在，请核对')
        return self.cleaned_data

class PickCourseForm(forms.Form):
    student_id = forms.CharField(error_messages={'required': '学号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)
    course_id = forms.CharField(error_messages={'required': '课程号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)

    def clean_student_id(self):
        id = self.cleaned_data['student_id']
        exists = Student.objects.filter(id=id).count()
        if exists == 0:
            raise forms.ValidationError('该学生未注册，请核对')
        return id

    def clean_course_id(self):
        id = self.cleaned_data['course_id']
        exists = Course.objects.filter(id=id).count()
        if exists == 0:
            raise forms.ValidationError('该课程不存在，请核对')
        return id

    def clean(self):
        student_id = self.cleaned_data['student_id']
        course_id = self.cleaned_data['course_id']
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
        if student in course.student.all():
            raise forms.ValidationError('该学生已选了这门课')
        picked_courses = student.course_set.all()
        for picked_course in picked_courses:
            for picked_course_time in picked_course.coursetime_set.all():
                for course_time in course.coursetime_set.all():
                    if (course_time.weekday == picked_course_time.weekday) and (course_time.end >= picked_course_time.begin) and (picked_course_time.end >= course_time.begin):
                        raise forms.ValidationError('与已选课程时间冲突')
        return self.cleaned_data

class DropCourseForm(forms.Form):
    student_id = forms.CharField(error_messages={'required': '学号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)
    course_id = forms.CharField(error_messages={'required': '课程号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)

    def clean_student_id(self):
        id = self.cleaned_data['student_id']
        exists = Student.objects.filter(id=id).count()
        if exists == 0:
            raise forms.ValidationError('该学生未注册，请核对')
        return id

    def clean_course_id(self):
        id = self.cleaned_data['course_id']
        exists = Course.objects.filter(id=id).count()
        if exists == 0:
            raise forms.ValidationError('该课程不存在，请核对')
        return id

    def clean(self):
        student_id = self.cleaned_data['student_id']
        course_id = self.cleaned_data['course_id']
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
        if student not in course.student.all():
            raise forms.ValidationError('该学生未选这门课')
        return self.cleaned_data

class AddCourseTeacherForm(forms.Form):
    teacher_id = forms.CharField(error_messages={'required': '教师工号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)
    course_id = forms.CharField(error_messages={'required': '课程号不能为空', 'max_length': '最多为 20 个字符'}, max_length=20)

    def clean_teacher_id(self):
        id = self.cleaned_data['teacher_id']
        exists = Teacher.objects.filter(id=id).count()
        if exists == 0:
            raise forms.ValidationError('该教师未注册，请核对')
        return id

    def clean_course_id(self):
        id = self.cleaned_data['course_id']
        exists = Course.objects.filter(id=id).count()
        if exists == 0:
            raise forms.ValidationError('该课程不存在，请核对')
        return id

    def clean(self):
        teacher_id = self.cleaned_data['teacher_id']
        course_id = self.cleaned_data['course_id']
        teacher = Teacher.objects.get(id=teacher_id)
        course = Course.objects.get(id=course_id)
        if teacher in course.teacher.all():
            raise forms.ValidationError('该教师已负责这门课')
        return self.cleaned_data
