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

    test_manager_id = 'm001'
    test_manager_name = 'test_manager'

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

    def setUp(self):
        self.first_student_request = self.create_one_student_register_request()
        self.first_student_response = register(self.first_student_request)

        self.first_teacher_request = self.create_one_teacher_register_request()
        self.first_teacher_response = register(self.first_teacher_request)

        self.first_manager_request = self.create_one_manager_register_request()
        self.first_manager_response = register(self.first_manager_request)

    # Student Tests
    def create_one_student_register_request(self):
        request = self.create_register_request(
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

    # Teacher Tests
    def create_one_teacher_register_request(self):
        request = self.create_register_request(
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
