from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views
from accounts.forms import LoginForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'register/', views.register, name='register'),
]
