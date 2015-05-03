# encoding: utf-8

from django.test import TestCase, Client
from django.http import HttpRequest
from django.conf import settings
from django.utils.importlib import import_module

from django.contrib.auth.models import User, Permission

from accounts.models import Student, Teacher, Manager
from accounts.views import register
from accounts.forms import RegisterForm

TEST_STUDENT_ID = 's001'
TEST_STUDENT_NAME = 'test_student'

TEST_TEACHER_ID = 't001'
TEST_TEACHER_NAME = 'test_teacher'
TEST_TEACHER_TITLE = 'test_title'

TEST_MANAGER_ID = 'm001'
TEST_MANAGER_NAME = 'test_manager'

TEST_PASSWORD = 'password'

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
    def setUp(self):
        self.first_student_request = self.create_one_student_register_request()
        self.first_student_response = register(self.first_student_request)

    def create_one_student_register_request(self):
        request = create_register_request(
            TEST_STUDENT_ID,
            TEST_STUDENT_NAME,
            TEST_PASSWORD,
            Student.user_type,
        )
        return request

    def test_student_register_create_correct_user(self):
        user = User.objects.filter(username=TEST_STUDENT_ID)
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, TEST_STUDENT_ID)
        self.assertTrue(first_user.check_password(TEST_PASSWORD))

    def test_student_register_create_correct_student(self):
        student = Student.objects.filter(id=TEST_STUDENT_ID)
        self.assertEqual(student.count(), 1)

        first_student = student[0]
        self.assertEqual(first_student.id, TEST_STUDENT_ID)
        self.assertEqual(first_student.name, TEST_STUDENT_NAME)

    def test_student_register_create_correct_student_user_relation(self):
        saved_user = User.objects.get(username=TEST_STUDENT_ID)
        saved_student = Student.objects.get(id=TEST_STUDENT_ID)

        self.assertEqual(saved_student, saved_user.student)

    def test_student_register_create_user_with_correct_permissions(self):
        saved_user = User.objects.get(username=TEST_STUDENT_ID)

        client = Client()
        login = client.login(username=saved_user.username, password=TEST_PASSWORD)

        self.assertTrue(saved_user.has_perm('courses.change_course'))

class TeacherRegisterTest(TestCase):
    def setUp(self):
        self.first_teacher_request = self.create_one_teacher_register_request()
        self.first_teacher_response = register(self.first_teacher_request)

    def create_one_teacher_register_request(self):
        request = create_register_request(
            TEST_TEACHER_ID,
            TEST_TEACHER_NAME,
            TEST_PASSWORD,
            Teacher.user_type,
        )
        request.POST['title'] = TEST_TEACHER_TITLE
        return request

    def test_teacher_register_create_correct_user(self):
        user = User.objects.filter(username=TEST_TEACHER_ID)
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, TEST_TEACHER_ID)
        self.assertTrue(first_user.check_password(TEST_PASSWORD))

    def test_teacher_register_create_correct_teacher(self):
        teacher = Teacher.objects.filter(id=TEST_TEACHER_ID)
        self.assertEqual(teacher.count(), 1)

        first_teacher = teacher[0]
        self.assertEqual(first_teacher.id, TEST_TEACHER_ID)
        self.assertEqual(first_teacher.name, TEST_TEACHER_NAME)

    def test_teacher_register_create_correct_teacher_user_relation(self):
        saved_user = User.objects.get(username=TEST_TEACHER_ID)
        saved_teacher = Teacher.objects.get(id=TEST_TEACHER_ID)

        self.assertEqual(saved_teacher, saved_user.teacher)

    def test_teacher_register_create_user_with_correct_permissions(self):
        saved_user = User.objects.get(username=TEST_TEACHER_ID)

        client = Client()
        login = client.login(username=saved_user.username, password=saved_user.password)

        # print saved_user.get_all_permissions()
        self.assertTrue(saved_user.has_perm('courses.change_course'))

class ManagerRegisterTest(TestCase):
    def setUp(self):
        self.first_manager_request = self.create_one_manager_register_request()
        self.first_manager_response = register(self.first_manager_request)

    def create_one_manager_register_request(self):
        request = create_register_request(
            TEST_MANAGER_ID,
            TEST_MANAGER_NAME,
            TEST_PASSWORD,
            Manager.user_type,
        )
        return request

    def test_manager_register_create_correct_user(self):
        user = User.objects.filter(username=TEST_MANAGER_ID)
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, TEST_MANAGER_ID)
        self.assertTrue(first_user.check_password(TEST_PASSWORD))

    def test_manager_register_create_correct_manager(self):
        manager = Manager.objects.filter(id=TEST_MANAGER_ID)
        self.assertEqual(manager.count(), 1)

        first_manager = manager[0]
        self.assertEqual(first_manager.id, TEST_MANAGER_ID)
        self.assertEqual(first_manager.name, TEST_MANAGER_NAME)

    def test_manager_register_create_correct_manager_user_relation(self):
        saved_user = User.objects.get(username=TEST_MANAGER_ID)
        saved_manager = Manager.objects.get(id=TEST_MANAGER_ID)

        self.assertEqual(saved_manager, saved_user.manager)

    def test_manager_register_create_user_with_correct_permissions(self):
        saved_user = User.objects.get(username=TEST_MANAGER_ID)

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
    def setUp(self):
        self.test_student = Student.objects.create(
            id=TEST_STUDENT_ID,
            name=TEST_STUDENT_NAME,
            user=User.objects.create_user(username=TEST_STUDENT_ID, password=TEST_PASSWORD)
        )

        self.test_teacher = Teacher.objects.create(
            id=TEST_TEACHER_ID,
            name=TEST_TEACHER_NAME,
            user=User.objects.create_user(username=TEST_TEACHER_ID, password=TEST_PASSWORD),
            title=TEST_TEACHER_TITLE,
        )

        self.test_manager = Manager.objects.create(
            id=TEST_MANAGER_ID,
            name=TEST_MANAGER_NAME,
            user=User.objects.create_user(username=TEST_MANAGER_ID, password=TEST_PASSWORD)
        )

    def test_student_login(self):
        response = self.client.post('/accounts/login/',
                                    {
                                        'username': TEST_STUDENT_ID,
                                        'password': TEST_PASSWORD,
                                    })
        self.assertIn('/courses/student/', response.url)

    def test_teacher_login(self):
        response = self.client.post('/accounts/login/',
                                    {
                                        'username': TEST_TEACHER_ID,
                                        'password': TEST_PASSWORD,
                                    })
        self.assertIn('/courses/teacher/', response.url)

    def test_manager_login(self):
        response = self.client.post('/accounts/login/',
                                    {
                                        'username': TEST_MANAGER_ID,
                                        'password': TEST_PASSWORD,
                                    })
        self.assertIn('/courses/manager/', response.url)
