from django.test import TestCase
from django.http import HttpRequest

from django.contrib.auth.models import User

from accounts.models import Student, Teacher, Manager
from accounts.views import register

class RegisterTest(TestCase):
    test_student_id = 's001'
    test_student_name = 'test_student'

    test_teacher_id = 't001'
    test_teacher_name = 'test_teacher'
    test_teacher_title = 'test_title'

    test_password = '1234'

    def create_register_request(self, id, name, password, type):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'id'       : id,
            'name'     : name,
            'password' : password,
            'type'     : type,
        }
        return request

    # Student Tests
    def create_one_student_register_request(self):
        request = self.create_register_request(
            self.test_student_id,
            self.test_student_name,
            self.test_password,
            'student',
        )
        return request

    def test_student_register_create_correct_user(self):
        request = self.create_one_student_register_request()

        response = register(request)

        user = User.objects.all()
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, self.test_student_id)
        self.assertTrue(first_user.check_password(self.test_password))

    def test_student_register_create_correct_student(self):
        request = self.create_one_student_register_request()

        response = register(request)

        student = Student.objects.all()
        self.assertEqual(student.count(), 1)

        first_student = student[0]
        self.assertEqual(first_student.id, self.test_student_id)
        self.assertEqual(first_student.name, self.test_student_name)

    def test_student_register_create_correct_student_user_relation(self):
        request = self.create_one_student_register_request()

        response = register(request)

        saved_user = User.objects.all()[0]
        saved_student = Student.objects.all()[0]

        self.assertEqual(saved_student, saved_user.student)

    # Teacher Tests
    def create_one_teacher_register_request(self):
        request = self.create_register_request(
            self.test_teacher_id,
            self.test_teacher_name,
            self.test_password,
            'teacher',
        )
        request.POST['title'] = self.test_teacher_title
        return request

    def test_teacher_register_create_correct_user(self):
        request = self.create_one_teacher_register_request()

        response = register(request)

        user = User.objects.all()
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, 't001')
        self.assertTrue(first_user.check_password(self.test_password))

    def test_teacher_register_create_correct_teacher(self):
        request = self.create_one_teacher_register_request()

        response = register(request)

        teacher = Teacher.objects.all()
        self.assertEqual(teacher.count(), 1)

        first_teacher = teacher[0]
        self.assertEqual(first_teacher.id, self.test_teacher_id)
        self.assertEqual(first_teacher.name, self.test_teacher_name)

    def test_teacher_register_create_correct_teacher_user_relation(self):
        request = self.create_one_teacher_register_request()

        response = register(request)

        saved_user = User.objects.all()[0]
        saved_teacher = Teacher.objects.all()[0]

        self.assertEqual(saved_teacher, saved_user.teacher)

    # Manager Tests
    def create_one_manager_register_request(self):
        request = self.create_register_request(
            self.test_manager_id,
            self.test_manager_name,
            self.test_password,
            Manager.user_type,
        )
        return request

    def test_manager_register_create_correct_user(self):
        request = self.create_one_manager_register_request()

        response = register(request)

        user = User.objects.all()
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, self.test_manager_id)
        self.assertTrue(first_user.check_password(self.test_password))

    def test_manager_register_create_correct_manager(self):
        request = self.create_one_manager_register_request()

        response = register(request)

        manager = Manager.objects.all()
        self.assertEqual(manager.count(), 1)

        first_manager = manager[0]
        self.assertEqual(first_manager.id, self.test_manager_id)
        self.assertEqual(first_manager.name, self.test_manager_name)

    def test_manager_register_create_correct_manager_user_relation(self):
        request = self.create_one_manager_register_request()

        response = register(request)

        saved_user = User.objects.all()[0]
        saved_manager = Manager.objects.all()[0]

        self.assertEqual(saved_manager, saved_user.manager)
