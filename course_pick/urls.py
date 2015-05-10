from django.conf.urls import include, url
from django.contrib import admin

from course_pick.views import homepage

urlpatterns = [
    # Examples:
    # url(r'^$', 'course_pick.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', homepage, name='homepage'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^courses/', include('courses.urls', namespace='courses')),
]
