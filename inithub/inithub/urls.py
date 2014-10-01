'''

@author: rtermondt
'''

from django.conf.urls import patterns, include, url
from inithub import settings
from manager.views.public import about, invitation

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^manager/', include('manager.urls')),
                       url(r'^support/', include('support.urls')),
                       url(r'^$', about),
                       url(r'^invitation/$', invitation),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$',
                             'django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}),
                            (r'^admin/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT}),
                            )
