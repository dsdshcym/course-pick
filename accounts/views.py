from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group

from accounts.models import Student, Teacher, Manager

def register(request):
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        password = request.POST['password']
        type = request.POST['type']
        new_user = User.objects.create_user(username=id, password=password)

        if type == Student.user_type:
            new_student = Student.objects.create(id = id, user=new_user, name=name)

        if type == Teacher.user_type:
            title = request.POST['title']
            new_teacher = Teacher.objects.create(id = id, user=new_user, name=name, title=title)

        if type == Manager.user_type:
            new_manager = Manager.objects.create(id = id, user=new_user, name=name)

        return redirect('/')
