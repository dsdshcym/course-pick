from django.test import TestCase, Client
from django.http import HttpRequest
from django.core import exceptions

from accounts.models import Student
from accounts.views import register
from accounts.tests import create_register_request

from courses.models import Course
from courses.views import add_course, delete_course, pick_course

def add_a_new_course_through_request(id, name, college, classroom, score, max_student_number, remark):
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {
        'id'                 : id,
        'name'               : name,
        'college'            : college,
        'classroom'          : classroom,
        'score'              : score,
        'max_student_number' : max_student_number,
        'remark'             : remark,
    }
    response = add_course(request)
    return response

class CourseModelTest(TestCase):

    def test_saving_and_retriving_courses(self):
        first_course = Course.objects.create(
            id='0001',
            name='first_test_course',
            score=2.0,
            max_student_number=50)

        second_course = Course.objects.create(
            id='0002',
            name='second_test_course',
            score=3.0,
            max_student_number=10)

        saved_courses = Course.objects.all()
        self.assertEqual(saved_courses.count(), 2)

        first_saved_item = saved_courses[0]
        second_saved_item = saved_courses[1]
        self.assertEqual(first_saved_item.name, 'first_test_course')
        self.assertEqual(second_saved_item.name, 'second_test_course')

class AddCourseViewTest(TestCase):

    def test_manager_can_add_a_new_course(self):
        response = add_a_new_course_through_request(
            '0001',
            'test',
            'CS',
            'Z2101',
            2.0,
            20,
            '',
        )
        self.assertEqual(Course.objects.count(), 1)
        new_course = Course.objects.first()
        self.assertEqual(new_course.name, 'test')

class DeleteCourseViewTest(TestCase):
    def setUp(self):
        new_course = Course.objects.create(
            id='c0001',
            name='test_course',
            college='CS',
            classroom='Z2101',
            score=2.0,
            max_student_number=50,
            remark='',
        )

    def test_manager_can_delete_a_exists_course(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'id': 'c0001',
        }

        response = delete_course(request)

        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Course.objects.get(id='c0001')

class PickCourseViewTest(TestCase):
    def setUp(self):
        self.add_course_response = add_a_new_course_through_request(
            'c0001',
            'test',
            'CS',
            'Z2101',
            2.0,
            20,
            '',
        )
        self.test_course = Course.objects.get(id='c0001')

        add_student_request = create_register_request(
            id='s0001',
            name='test_student',
            password='',
            type=Student.user_type
        )

        add_student_response = register(add_student_request)

        self.test_student = Student.objects.get(id='s0001')

    def test_a_student_can_pick_a_course(self):
        client = Client()
        client.login(username=self.test_student.id, password='')

        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'student_id': self.test_student.id,
            'course_id': self.test_course.id,
        }
        response = pick_course(request)

        self.assertEqual(self.test_course.student.count(), 1)
        self.assertEqual(self.test_course.student.first(), self.test_student)
