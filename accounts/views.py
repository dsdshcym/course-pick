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

        if type == 'student':
            new_student = Student.objects.create(id = id, user=new_user, name=name)

        if type == 'teacher':
            title = request.POST['title']
            new_teacher = Teacher.objects.create(id = id, user=new_user, name=name, title=title)
        return redirect('/')
