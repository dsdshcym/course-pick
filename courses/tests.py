import datetime

from django.test import TestCase, Client
from django.http import HttpRequest
from django.core import exceptions
from django.utils import timezone

from django.contrib.auth.models import User

from accounts.models import Student, Teacher, Manager
from accounts.views import register
from accounts.tests import create_register_request

from courses.models import Course, CourseTime, Exam
from courses.views import add_course, delete_course, pick_course

def add_a_new_course_through_request(
        id,
        name,
        college,
        classroom,
        score,
        max_student_number,
        remark,
        teacher=[],
        time=[],
        exam=None,
):
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
        'time'               : time,
        'exam'               : exam,
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

        self.time = {
            'weekday': 'Mon',
            'begin': 1,
            'end': 4,
        }

        time_list = [self.time]

        self.exam = {
            'method': Exam.KJ,
            'date': timezone.now().date(),
            'time': timezone.now().time(),
        }

        self.response = add_a_new_course_through_request(
            'c0001',
            'test',
            'CS',
            'Z2101',
            2.0,
            20,
            '',
            teacher_list,
            time_list,
            self.exam,
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

    def test_add_a_new_course_need_time_info(self):
        saved_course = Course.objects.get(id='c0001')
        course_time = CourseTime.objects.all()
        self.assertEqual(course_time.count(), 1)
        self.assertEqual(course_time.first().course, saved_course)
        self.assertEqual(course_time.first().weekday, self.time['weekday'])
        self.assertEqual(course_time.first().begin, self.time['begin'])
        self.assertEqual(course_time.first().end, self.time['end'])

    def test_add_a_new_course_need_exam_info(self):
        saved_course = Course.objects.get(id='c0001')
        exam = Exam.objects.all()
        self.assertEqual(exam.count(), 1)
        self.assertEqual(exam.first().course, saved_course)
        self.assertEqual(exam.first().method, self.exam['method'])
        self.assertEqual(exam.first().date, self.exam['date'])
        self.assertEqual(exam.first().time, self.exam['time'])

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

class PickCourseViewTest(TestCase):
    def setUp(self):
        self.test_teacher = Teacher.objects.create(
            id='t0001',
            name='test_teacher',
            user=User.objects.create(username='t0001',password=''),
        )

        self.test_course = Course.objects.create(
            id='c0001',
            name='test',
            score=2.0,
            max_student_number=50,
        )
        self.test_course.teacher.add(self.test_teacher)

        self.test_student = Student.objects.create(
            id='s0001',
            name='test_student',
            user=User.objects.create(username='s0001', password=''),
            )

        self.test_manager = Manager.objects.create(
            id='m0001',
            name='test_manager',
            user=User.objects.create(username='m0001', password=''),
            )

    def test_a_student_can_pick_a_course(self):
        self.client.login(username=self.test_student.id, password='')

        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'student_id': self.test_student.id,
            'course_id': self.test_course.id,
        }
        request.user = User.objects.get(student=self.test_student)
        response = pick_course(request)

        self.assertEqual(self.test_course.student.count(), 1)
        self.assertEqual(self.test_course.student.first(), self.test_student)

    def test_a_teacher_can_pick_his_course_for_a_student(self):
        self.client.login(username=self.test_teacher.id, password='')

        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'student_id': self.test_student.id,
            'course_id': self.test_course.id,
        }
        request.user = User.objects.get(teacher=self.test_teacher)
        response = pick_course(request)

        self.assertEqual(self.test_course.student.count(), 1)
        self.assertEqual(self.test_course.student.first(), self.test_student)

    def test_a_manager_can_pick_any_course_for_any_student(self):
        self.client.login(username=self.test_manager.id, password='')

        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'student_id': self.test_student.id,
            'course_id': self.test_course.id,
        }
        request.user = User.objects.get(manager=self.test_manager)
        response = pick_course(request)

        self.assertEqual(self.test_course.student.count(), 1)
        self.assertEqual(self.test_course.student.first(), self.test_student)

class DropCourseViewTest(TestCase):
    def setUp(self):
        self.first_test_student = Student.objects.create(
            id='s0001',
            name='test_student',
            user=User.objects.create_user(username='s0001', password='')
        )
        self.test_course = Course.objects.create(
            id='c0001',
            name='test_course',
            score=2.0,
            max_student_number=50,
        )
        self.test_course.student.add(self.first_test_student)

    def test_a_student_can_drop_a_picked_course(self):
        student_id = self.first_test_student.id
        course_id = self.test_course.id

        self.client.login(username=student_id, password='')

        self.assertEqual(self.test_course.student.count(), 1)

        response = self.client.post('/courses/drop/', {'student_id': student_id, 'course_id': course_id})

        self.assertEqual(self.test_course.student.count(), 0)
