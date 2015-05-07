from django.conf.urls import url

from courses import views

urlpatterns = [
    url(r'^add/$', views.add_course, name='add'),
    url(r'^edit/(?P<course_id>.*)', views.edit_course, name='edit_course'),
    url(r'^pick/$', views.pick_course, name='pick'),
    url(r'^drop/$', views.drop_course, name='drop'),
    url(r'^delete/$', views.delete_course, name='delete'),
    url(r'^search/', views.search_course, name='search'),
    url(r'^student/$', views.student_view, name='student_view'),
    url(r'^teacher/$', views.teacher_view, name='teacher_view'),
    url(r'^manager/$', views.manager_view, name='manager_view'),
    url(r'^add/teacher/(?P<course_id>.*)', views.add_course_teacher, name='add_course_teacher'),
    url(r'^add/coursetime/(?P<course_id>.*)', views.add_coursetime, name='add_coursetime'),
    url(r'^add/exam/(?P<course_id>.*)', views.add_exam, name='add_exam'),
    url(r'^detail/(?P<course_id>.*)', views.detail, name='detail'),
    url(r'^extra/(?P<course_id>.*)', views.extra_info, name='extra_info'),
    url(r'^clear_teacher/', views.clear_teacher, name='clear_teacher'),
]
