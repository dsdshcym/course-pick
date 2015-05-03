from django.conf.urls import url

from courses import views

urlpatterns = [
    url(r'^add/$', views.add_course, name='add'),
    url(r'^drop/$', views.drop_course, name='drop'),
    url(r'^delete/$', views.delete_course, name='delete'),
    url(r'^search/(?P<search_content>.*)', views.search_course, name='search'),
    url(r'^student/$', views.student_view, name='student_view'),
    url(r'^add/teacher/(?P<course_id>.*)', views.add_course_teacher, name='add_teacher'),
    url(r'^add/coursetime/(?P<course_id>.*)', views.add_coursetime, name='add_teacher'),
]
