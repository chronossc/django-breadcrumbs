from django.conf.urls import patterns, include
from .views import page1
# special urls for flatpage test cases
urlpatterns = patterns('',
    (r'^page1/', page1),
)

