from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sample_d14.views.home', name='home'),
    # url(r'^sample_d14/', include('sample_d14.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webui.views.home', name='home'),
    url(r'^someview/$', 'webui.views.someview', name='someview'),
    (r'^pages/', include('breadcrumbs.urls')),
)

urlpatterns += patterns('breadcrumbs.views',
    (r'^pages2/(?P<url>.*)$', 'flatpage'),
    url(r'^license/$', 'flatpage', {'url': '/flat04/'}, name='license'),
)
