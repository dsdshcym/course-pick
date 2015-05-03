from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views
from accounts.forms import LoginForm

urlpatterns = [
    url(r'register/', views.register, name='register'),
    url(r'login/', views.login, name='login'),
]
