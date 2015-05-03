# encoding: utf-8

from django import forms

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
