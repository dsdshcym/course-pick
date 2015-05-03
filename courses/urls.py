from django.conf.urls import url

from courses import views

urlpatterns = [
    url(r'^drop/$', views.drop_course, name='drop'),
    url(r'^delete/$', views.delete_course, name='delete'),
    url(r'^search/(?P<search_content>.*)', views.search_course, name='search'),
    url(r'^student/$', views.student_view, name='student_view'),
]
