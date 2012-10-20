import django
if django.get_version().startswith('1.4'):
    from django.conf.urls import patterns
else:
    from django.conf.urls.defaults import patterns
from .views import page1
# special urls for flatpage test cases
urlpatterns = patterns('',
    (r'^page1/', page1),
)

