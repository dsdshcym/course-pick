# encoding: utf-8

from django.test import TestCase, Client
from django.http import HttpRequest
from django.conf import settings
from django.utils.importlib import import_module

from django.contrib.auth.models import User, Permission

from accounts.models import Student, Teacher, Manager
from accounts.views import register
from accounts.forms import RegisterForm

def create_register_request(id, name, password, type, title=''):
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {
        'id'       : id,
        'name'     : name,
        'password' : password,
        'confirm_password' : password,
        'type'     : type,
        'title'    : title,
    }
    engine = import_module(settings.SESSION_ENGINE)
    session_key = None
    request.session = engine.SessionStore(session_key)
    return request

class StudentRegisterTest(TestCase):
    test_student_id = 's001'
    test_student_name = 'test_student'

    test_password = 'password'

    def setUp(self):
        self.first_student_request = self.create_one_student_register_request()
        self.first_student_response = register(self.first_student_request)

    def create_one_student_register_request(self):
        request = create_register_request(
            self.test_student_id,
            self.test_student_name,
            self.test_password,
            Student.user_type,
        )
        return request

    def test_student_register_create_correct_user(self):
        user = User.objects.filter(username=self.test_student_id)
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, self.test_student_id)
        self.assertTrue(first_user.check_password(self.test_password))

    def test_student_register_create_correct_student(self):
        student = Student.objects.filter(id=self.test_student_id)
        self.assertEqual(student.count(), 1)

        first_student = student[0]
        self.assertEqual(first_student.id, self.test_student_id)
        self.assertEqual(first_student.name, self.test_student_name)

    def test_student_register_create_correct_student_user_relation(self):
        saved_user = User.objects.get(username=self.test_student_id)
        saved_student = Student.objects.get(id=self.test_student_id)

        self.assertEqual(saved_student, saved_user.student)

    def test_student_register_create_user_with_correct_permissions(self):
        saved_user = User.objects.get(username=self.test_student_id)

        client = Client()
        login = client.login(username=saved_user.username, password=self.test_password)

        self.assertTrue(saved_user.has_perm('courses.change_course'))

class TeacherRegisterTest(TestCase):
    test_teacher_id = 't001'
    test_teacher_name = 'test_teacher'
    test_teacher_title = 'test_title'

    test_password = 'password'

    def setUp(self):
        self.first_teacher_request = self.create_one_teacher_register_request()
        self.first_teacher_response = register(self.first_teacher_request)

    def create_one_teacher_register_request(self):
        request = create_register_request(
            self.test_teacher_id,
            self.test_teacher_name,
            self.test_password,
            Teacher.user_type,
        )
        request.POST['title'] = self.test_teacher_title
        return request

    def test_teacher_register_create_correct_user(self):
        user = User.objects.filter(username=self.test_teacher_id)
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, self.test_teacher_id)
        self.assertTrue(first_user.check_password(self.test_password))

    def test_teacher_register_create_correct_teacher(self):
        teacher = Teacher.objects.filter(id=self.test_teacher_id)
        self.assertEqual(teacher.count(), 1)

        first_teacher = teacher[0]
        self.assertEqual(first_teacher.id, self.test_teacher_id)
        self.assertEqual(first_teacher.name, self.test_teacher_name)

    def test_teacher_register_create_correct_teacher_user_relation(self):
        saved_user = User.objects.get(username=self.test_teacher_id)
        saved_teacher = Teacher.objects.get(id=self.test_teacher_id)

        self.assertEqual(saved_teacher, saved_user.teacher)

    def test_teacher_register_create_user_with_correct_permissions(self):
        saved_user = User.objects.get(username=self.test_teacher_id)

        client = Client()
        login = client.login(username=saved_user.username, password=saved_user.password)

        # print saved_user.get_all_permissions()
        self.assertTrue(saved_user.has_perm('courses.change_course'))

class ManagerRegisterTest(TestCase):
    test_manager_id = 'm001'
    test_manager_name = 'test_manager'

    test_password = 'password'

    def setUp(self):
        self.first_manager_request = self.create_one_manager_register_request()
        self.first_manager_response = register(self.first_manager_request)

    def create_one_manager_register_request(self):
        request = create_register_request(
            self.test_manager_id,
            self.test_manager_name,
            self.test_password,
            Manager.user_type,
        )
        return request

    def test_manager_register_create_correct_user(self):
        user = User.objects.filter(username=self.test_manager_id)
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, self.test_manager_id)
        self.assertTrue(first_user.check_password(self.test_password))

    def test_manager_register_create_correct_manager(self):
        manager = Manager.objects.filter(id=self.test_manager_id)
        self.assertEqual(manager.count(), 1)

        first_manager = manager[0]
        self.assertEqual(first_manager.id, self.test_manager_id)
        self.assertEqual(first_manager.name, self.test_manager_name)

    def test_manager_register_create_correct_manager_user_relation(self):
        saved_user = User.objects.get(username=self.test_manager_id)
        saved_manager = Manager.objects.get(id=self.test_manager_id)

        self.assertEqual(saved_manager, saved_user.manager)

    def test_manager_register_create_user_with_correct_permissions(self):
        saved_user = User.objects.get(username=self.test_manager_id)

        client = Client()
        login = client.login(username=saved_user.username, password=saved_user.password)

        # print saved_user.get_all_permissions()
        self.assertTrue(saved_user.has_perm('courses.add_course'))
        self.assertTrue(saved_user.has_perm('courses.change_course'))
        self.assertTrue(saved_user.has_perm('courses.delete_course'))

class RegisterFormTest(TestCase):
    def setUp(self):
        self.test_form = RegisterForm({
            'id': '123'
        })

    def test_fileds_errors(self):
        # self.assertFieldOutput(self.test_form.password, {'', u'学号/工号不能为空'})
        pass

class LoginViewTest(TestCase):
    test_student_id = 's001'
    test_student_name = 'test_student'

    test_teacher_id = 't001'
    test_teacher_name = 'test_teacher'
    test_teacher_title = 'test_title'

    test_manager_id = 'm001'
    test_manager_name = 'test_manager'

    test_password = 'password'

    def setUp(self):
        self.test_student = Student.objects.create(
            id=self.test_student_id,
            name=self.test_student_name,
            user=User.objects.create_user(username=self.test_student_id, password=self.test_password)
        )

        self.test_teacher = Teacher.objects.create(
            id=self.test_teacher_id,
            name=self.test_teacher_name,
            user=User.objects.create_user(username=self.test_teacher_id, password=self.test_password),
            title=self.test_teacher_title,
        )

        self.test_manager = Manager.objects.create(
            id=self.test_manager_id,
            name=self.test_manager_name,
            user=User.objects.create_user(username=self.test_manager_id, password=self.test_password)
        )

    def test_student_login(self):
        response = self.client.post('/accounts/login/',
                                    {
                                        'username': self.test_student_id,
                                        'password': self.test_password,
                                    })
        self.assertIn('/accounts/student/', response.url)

    def test_teacher_login(self):
        response = self.client.post('/accounts/login/',
                                    {
                                        'username': self.test_teacher_id,
                                        'password': self.test_password,
                                    })
        self.assertIn('/accounts/teacher/', response.url)

    def test_manager_login(self):
        response = self.client.post('/accounts/login/',
                                    {
                                        'username': self.test_manager_id,
                                        'password': self.test_password,
                                    })
        self.assertIn('/accounts/manager/', response.url)
