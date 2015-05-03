import datetime

from django.test import TestCase, Client
from django.http import HttpRequest
from django.core import exceptions
from django.utils import timezone

from django.contrib.auth.models import User

from accounts.models import Student, Teacher, Manager
from accounts.views import register, MANAGER_PERMISSION
from accounts.tests import create_register_request

from courses.models import Course, CourseTime, Exam
from courses.views import add_course, delete_course, pick_course, search_course

TEST_STUDENT_ID = 's001'
TEST_STUDENT_NAME = 'test_student'

TEST_TEACHER_ID = 't001'
TEST_TEACHER_NAME = 'test_teacher'
TEST_TEACHER_TITLE = 'test_title'

TEST_MANAGER_ID = 'm001'
TEST_MANAGER_NAME = 'test_manager'

TEST_PASSWORD = 'password'

TEST_COURSE_ID = 'c001'
TEST_COURSE_NAME = 'test_course'
TEST_COURSE_COLLEGE = 'CS'
TEST_COURSE_CLASSROOM = 'Z2101'
TEST_COURSE_SCORE = 2.0
TEST_COURSE_MAX_STUDENT_NUMBER = 50
TEST_COURSE_REMARK = ''

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
        self.manager = Manager.objects.create(
            id=TEST_MANAGER_ID,
            name=TEST_MANAGER_NAME,
            user=User.objects.create_user(username=TEST_MANAGER_ID, password=TEST_PASSWORD),
        )

        self.manager.user.user_permissions = MANAGER_PERMISSION

    def test_manager_can_add_a_new_course(self):
        self.client.login(username=TEST_MANAGER_ID, password=TEST_PASSWORD)
        self.client.post('/courses/add/', {
            'id'                 : TEST_COURSE_ID,
            'name'               : TEST_COURSE_NAME,
            'college'            : TEST_COURSE_COLLEGE,
            'classroom'          : TEST_COURSE_CLASSROOM,
            'score'              : TEST_COURSE_SCORE,
            'max_student_number' : TEST_COURSE_MAX_STUDENT_NUMBER,
            'remark'             : TEST_COURSE_REMARK,
        })
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 1)
        new_course = courses.first()
        self.assertEqual(new_course.name, TEST_COURSE_NAME)

    # def test_add_a_new_course_need_teacher_info(self):
    #     saved_course = Course.objects.get(id='c0001')
    #     self.assertEqual(saved_course.teacher.count(), 1)
    #     self.assertEqual(saved_course.teacher.first(), self.teacher)

    # def test_add_a_new_course_need_time_info(self):
    #     saved_course = Course.objects.get(id='c0001')
    #     course_time = CourseTime.objects.all()
    #     self.assertEqual(course_time.count(), 1)
    #     self.assertEqual(course_time.first().course, saved_course)
    #     self.assertEqual(course_time.first().weekday, self.time['weekday'])
    #     self.assertEqual(course_time.first().begin, self.time['begin'])
    #     self.assertEqual(course_time.first().end, self.time['end'])

    # def test_add_a_new_course_need_exam_info(self):
    #     saved_course = Course.objects.get(id='c0001')
    #     exam = Exam.objects.all()
    #     self.assertEqual(exam.count(), 1)
    #     self.assertEqual(exam.first().course, saved_course)
    #     self.assertEqual(exam.first().method, self.exam['method'])
    #     self.assertEqual(exam.first().date, self.exam['date'])
    #     self.assertEqual(exam.first().time, self.exam['time'])

class AddCourseExtraInfoTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            id=TEST_TEACHER_ID,
            name=TEST_TEACHER_NAME,
            user=User.objects.create_user(username=TEST_TEACHER_ID, password=TEST_PASSWORD),
            title=TEST_TEACHER_TITLE,
        )

        self.course = Course.objects.create(
            id                 = TEST_COURSE_ID,
            name               = TEST_COURSE_NAME,
            college            = TEST_COURSE_COLLEGE,
            classroom          = TEST_COURSE_CLASSROOM,
            score              = TEST_COURSE_SCORE,
            max_student_number = TEST_COURSE_MAX_STUDENT_NUMBER,
            remark             = TEST_COURSE_REMARK,
        )

        self.manager = Manager.objects.create(
            id=TEST_MANAGER_ID,
            name=TEST_MANAGER_NAME,
            user=User.objects.create_user(username=TEST_MANAGER_ID, password=TEST_PASSWORD),
        )

        self.coursetime = {
            'weekday': 'Mon',
            'begin': 1,
            'end': 4,
        }

        self.exam = {
            'method': Exam.KJ,
            'date': timezone.now().date(),
            'time': timezone.now().time(),
        }

        self.client.login(username=TEST_MANAGER_ID, password=TEST_PASSWORD)

        self.manager.user.user_permissions = MANAGER_PERMISSION

    def test_a_manager_can_add_a_course_teacher(self):
        response = self.client.post('/courses/add/teacher/' + TEST_COURSE_ID, {
            'id': TEST_TEACHER_ID,
            'name': TEST_TEACHER_NAME,
        })

        added_teacher = self.course.teacher.all()

        self.assertEqual(added_teacher.count(), 1)
        self.assertEqual(added_teacher.first(), self.teacher)

    def test_a_manager_can_add_a_coursetime(self):
        response = self.client.post('/courses/add/coursetime/' + TEST_COURSE_ID, self.coursetime)

        added_coursetime = CourseTime.objects.all()

        self.assertEqual(added_coursetime.count(), 1)
        self.assertEqual(added_coursetime.first().course, self.course)
        self.assertEqual(added_coursetime.first().weekday, self.coursetime['weekday'])

    def test_a_manager_can_add_a_exam(self):
        response = self.client.post('/courses/add/exam/' + TEST_COURSE_ID, self.exam)

        added_exam = Exam.objects.all()

        self.assertEqual(added_exam.count(), 1)
        self.assertEqual(added_exam.first().course, self.course)
        self.assertEqual(added_exam.first().method, self.exam['method'])

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

        manager_user = User.objects.create_user(username='m0001', password='')

        self.test_manager = Manager.objects.create(
            id='m0001',
            name='test_manager',
            user=manager_user,
            )

        manager_user.user_permissions = MANAGER_PERMISSION

    def test_manager_can_delete_a_exists_course(self):
        self.client.login(username=self.test_manager.id, password='')
        self.client.post('/courses/delete/', {'id': self.new_course.id})

        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Course.objects.get(id=self.new_course.id)

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

        self.test_course_time = CourseTime.objects.create(
            course=self.test_course,
            weekday='Mon',
            begin=1,
            end=14,
        )

        self.another_test_course = Course.objects.create(
            id='c0002',
            name='test_another',
            score=2.0,
            max_student_number=50,
        )

        self.another_test_course_time = CourseTime.objects.create(
            course=self.another_test_course,
            weekday='Mon',
            begin=3,
            end=13,
        )

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

    def test_pick_course_solve_time_conflict(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'student_id': self.test_student.id,
            'course_id': self.test_course.id,
        }
        request.user = User.objects.get(student=self.test_student)
        first_response = pick_course(request)

        self.assertEqual(self.test_student.course_set.count(), 1)

        request.POST['course_id'] = self.another_test_course.id
        second_response = pick_course(request)

        self.assertEqual(self.test_student.course_set.count(), 1)

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

class SearchCourseTest(TestCase):
    def setUp(self):
        self.first_test_teacher = Teacher.objects.create(
            id='t0001',
            name='first_test_teacher',
            user=User.objects.create(username='t0001',password=''),
        )
        self.first_test_course = Course.objects.create(
            id='c0001',
            name='first_test_course',
            college='CS',
            score=2.0,
            max_student_number=50,
        )
        self.first_test_course.teacher.add(self.first_test_teacher)

        self.second_test_teacher = Teacher.objects.create(
            id='t0002',
            name='second_test_teacher',
            user=User.objects.create(username='t0002',password=''),
        )
        self.second_test_course = Course.objects.create(
            id='c0002',
            name='second_test_course',
            college='ME',
            score=2.0,
            max_student_number=50,
        )
        self.second_test_course.teacher.add(self.second_test_teacher)

    def test_search_for_a_class_with_course_name(self):
        response = self.client.get('/courses/search/first_test_course', )
        course_results = response.context['course_results']
        self.assertEqual(course_results.count(), 1)
        self.assertIn(self.first_test_course, course_results)

    def test_search_for_a_class_with_teachers_name(self):
        response = self.client.get('/courses/search/first_test_teacher', )
        teacher_results = response.context['teacher_results']
        self.assertEqual(teacher_results.count(), 1)
        self.assertIn(self.first_test_course, teacher_results)

    def test_search_for_a_class_with_college_name(self):
        response = self.client.get('/courses/search/cs', )
        college_results = response.context['college_results']
        self.assertEqual(college_results.count(), 1)
        self.assertIn(self.first_test_course, college_results)

class StudentViewTest(TestCase):
    def setUp(self):
        self.test_student = Student.objects.create(
            id=TEST_STUDENT_ID,
            name=TEST_STUDENT_NAME,
            user=User.objects.create_user(username=TEST_STUDENT_ID, password=TEST_PASSWORD)
        )
        self.test_course = Course.objects.create(
            id='c0001',
            name='test_course',
            score=2.0,
            max_student_number=50,
        )
        self.test_course_time = CourseTime.objects.create(
            course=self.test_course,
            weekday='Mon',
            begin=1,
            end=4,
        )
        self.test_course.student.add(self.test_student)
        self.client.login(username=TEST_STUDENT_ID, password=TEST_PASSWORD)

    def test_student_view_returns_picked_classes_info(self):
        response = self.client.get('/courses/student/')
        self.assertIn(self.test_course, response.context['courses'])

    def test_student_view_returns_class_table_info(self):
        response = self.client.get('/courses/student/')
        self.assertIn(self.test_course, response.context['class_table'][0])
