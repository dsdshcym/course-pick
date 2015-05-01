from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    # url(r'^login/$', views.login, name='login'),
]
