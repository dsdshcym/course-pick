from django.test import TestCase
from django.http import HttpRequest

from django.contrib.auth.models import User

from accounts.models import Student, Teacher, Manager
from accounts.views import register

class RegisterTest(TestCase):

    def test_student_register(self):
        test_student = Student(
            id='s001',
            name='test_stu'
        )

        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'id'       : test_student.id,
            'name'     : test_student.name,
            'password' : '1234',
            'type'     : 'student',
        }

        response = register(request)

        user = User.objects.all()
        self.assertEqual(user.count(), 1)

        first_user = user[0]
        self.assertEqual(first_user.username, 's001')
        self.assertTrue(first_user.check_password('1234'))

        saved_student = first_user.student
        self.assertEqual(saved_student.id, test_student.id)
        self.assertEqual(saved_student.name, test_student.name)

        student = Student.objects.all()
        self.assertEqual(student.count(), 1)

        first_student = student[0]
        self.assertEqual(first_student, saved_student)

        # self.assertTrue(first_user.check_password('1234'))
