from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login as auth_login

from django.template.response import TemplateResponse

from accounts.models import Student, Teacher, Manager
from accounts.forms import RegisterForm, LoginForm

STUDENT_PERMISSION = Permission.objects.filter(codename='change_course')
TEACHER_PERMISSION = Permission.objects.filter(codename='change_course')
MANAGER_PERMISSION = Permission.objects.filter(codename__endswith='course')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            id = request.POST['id']
            name = request.POST['name']
            password = request.POST['password']
            type = request.POST['type']
            new_user = User.objects.create_user(username=id, password=password)

            if type == Student.user_type:
                new_student = Student.objects.create(id = id, user=new_user, name=name)
                new_user.user_permissions = STUDENT_PERMISSION

            if type == Teacher.user_type:
                title = form.cleaned_data['title']
                new_teacher = Teacher.objects.create(id = id, user=new_user, name=name, title=title)
                new_user.user_permissions = TEACHER_PERMISSION

            if type == Manager.user_type:
                new_manager = Manager.objects.create(id = id, user=new_user, name=name)
                new_user.user_permissions = MANAGER_PERMISSION

            user = authenticate(username=id, password=password)
            auth_login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return TemplateResponse(request, "accounts/register.html", context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                auth_login(request, user)

            try:
                if user.student:
                    return redirect('/accounts/student/')
            except:
                pass

            try:
                if user.teacher:
                    return redirect('/accounts/teacher/')
            except:
                pass

            try:
                if user.manager:
                    return redirect('/accounts/manager/')
            except:
                pass
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return TemplateResponse(request, "accounts/login.html", context)
