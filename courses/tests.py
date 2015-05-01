from django.test import TestCase
from django.http import HttpRequest
from django.core import exceptions

from accounts.models import Teacher
from accounts.views import register
from accounts.tests import create_register_request

from courses.models import Course
from courses.views import add_course, delete_course

def add_a_new_course_through_request(id, name, college, classroom, score, max_student_number, remark, teacher=None):
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
        'teacher'            : teacher,
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
    def setUp(self):
        teacher_register_request = create_register_request(
            id='t0001',
            name='test_teacher',
            type=Teacher.user_type,
            password='',
        )

        teacher_register_request.POST['title'] = ''

        teacher_register_response = register(teacher_register_request)

        self.teacher = Teacher.objects.get(id='t0001')

        teacher_list = [self.teacher]

        self.response = add_a_new_course_through_request(
            'c0001',
            'test',
            'CS',
            'Z2101',
            2.0,
            20,
            '',
            teacher_list,
        )

    def test_manager_can_add_a_new_course(self):
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 1)
        new_course = courses.first()
        self.assertEqual(new_course.name, 'test')

    def test_add_a_new_course_need_teacher_info(self):
        saved_course = Course.objects.get(id='c0001')
        self.assertEqual(saved_course.teacher.count(), 1)
        self.assertEqual(saved_course.teacher.first(), self.teacher)

class DeleteCourseViewTest(TestCase):
    def setUp(self):
        self.new_course = Course(
            id='c0001',
            name='test_course',
            college='CS',
            classroom='Z2101',
            score=2.0,
            max_student_number=50,
            remark='',
        )
        self.new_course.save()

    def test_manager_can_delete_a_exists_course(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'id': self.new_course.id,
        }

        response = delete_course(request)

        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Course.objects.get(id='c0001')
