from django.conf.urls import patterns, url
from .views import (
    home, someview, CBVHome, CBVLevel1, CBVLevel2WithArgs
)

urlpatterns = patterns(
    '',
    url(r'^$', home),
    url(r'^someview/$', someview),
    url(r'^cbvhome/$', CBVHome.as_view()),
    url(r'^cbvhome/L1/$', CBVLevel1.as_view()),
    url(r'^cbvhome/L1/L2/(?P<num>[0-9])/$', CBVLevel2WithArgs.as_view()),
)
