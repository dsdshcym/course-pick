from django.test import TestCase
from django.http import HttpRequest

from courses.models import Course
from courses.views import add_course

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

class AddCourseTest(TestCase):

    def test_manager_can_add_a_new_course(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'id'                 : '0001',
            'name'               : 'test',
            'college'            : 'CS',
            'classroom'          : 'Z2101',
            'score'              : 2.0,
            'max_student_number' : 20,
            'remark'             : '',
        }

        print request.POST

        response = add_course(request)

        self.assertEqual(Course.objects.count(), 1)
        new_course = Course.objects.first()
        self.assertEqual(new_course.name, 'test')
