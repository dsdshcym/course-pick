# encoding: utf-8

import datetime, random

from django.utils import timezone
from django.contrib.auth.models import User

from courses.models import *
from accounts.models import *
from accounts.views import STUDENT_PERMISSION, TEACHER_PERMISSION, MANAGER_PERMISSION

WEEKDAY_CHOICES = [
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sun',
]

COLLEGE_CHOICES = [
    'CS',
    'ME',
    'EE',
    'MA',
]

CLASSROOM_CHOICES = [
    'Z2101',
    'Z2212',
    'Z2201',
    'Z2105',
    'Z2215',
    'Z2203',
]

EXAM_METHOD_CHOICES = [
    'KJ',
    'BJ',
    'LW',
]

TITLE_CHOICES = [
    '教授',
    '副教授',
    '研究员',
    '副研究员',
]

TEST_PASSWORD = '123123'

def make_test_student(n):
    for i in range(n):
        student_id = 's' + str(i)
        student_name = '学生' + str(i)

        new_user = User.objects.create_user(
            username = student_id,
            password = TEST_PASSWORD,
        )

        new_user.user_permissions = STUDENT_PERMISSION

        new_student = Student.objects.create(
            id = student_id,
            user = new_user,
            name = student_name,
        )

def make_test_teacher(n):
    for i in range(n):
        teacher_id = 't' + str(i)
        teacher_name = '教师' + str(i)

        new_user = User.objects.create_user(
            username = teacher_id,
            password = TEST_PASSWORD,
        )

        new_user.user_permissions = TEACHER_PERMISSION

        new_teacher = Teacher.objects.create(
            id = teacher_id,
            user = new_user,
            name = teacher_name,
            title = random.choice(TITLE_CHOICES)
        )

def make_test_manager(n):
    for i in range(n):
        manager_id = 'm' + str(i)
        manager_name = '教务员' + str(i)

        new_user = User.objects.create_user(
            username = manager_id,
            password = TEST_PASSWORD,
        )

        new_user.user_permissions = MANAGER_PERMISSION

        new_manager = Manager.objects.create(
            id = manager_id,
            user = new_user,
            name = manager_name,
        )

def make_full_random_courses():
    all_teacher = Teacher.objects.all()
    for weekday in WEEKDAY_CHOICES:
        for begin in range(1, 15):
            for end in range(begin, 15):
                new_course = Course.objects.create(
                    id                 = 'c/' + str(weekday) + '/' + str(begin) + '/' + str(end),
                    name               = '课程/' + str(weekday) + '/' + str(begin) + '/' + str(end),
                    college            = random.choice(COLLEGE_CHOICES),
                    classroom          = random.choice(CLASSROOM_CHOICES),
                    score              = 4.0 * random.random(),
                    max_student_number = random.randint(1, 100),
                    remark             = ''
                )

                new_coursetime = CourseTime.objects.create(
                    course = new_course,
                    weekday = weekday,
                    begin = begin,
                    end = end,
                )

                new_course.teacher.add(random.choice(all_teacher))

                new_exam_method = random.choice(EXAM_METHOD_CHOICES)
                new_exam_date = timezone.now() + datetime.timedelta(days=random.randint(30, 60))
                new_exam_time = timezone.now().time()

                new_exam = Exam.objects.create(
                    course = new_course,
                    method = new_exam_method,
                    date = new_exam_date,
                )

                if new_exam_method != 'LW':
                    new_exam.time = new_exam_time
                    new_exam.save()

User.objects.create_superuser(username='dsdshcym', password='123123', email='')

make_test_student(10)
make_test_teacher(10)
make_test_manager(10)
make_full_random_courses()
