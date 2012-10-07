from django.conf.urls import patterns

urlpatterns = patterns('breadcrumbs.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)
