'''

@author: rtermondt
'''
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('support.views',
                       url(r'^ticket/new/$',
                           'ticket_new'),
                       url(r'^ticket/item/new/(?P<ticket_id>\d+)/$',
                           'item_new'),
                       url(r'^ticket/item/new/$',
                           'item_new'),
                       url(r'^ticket/list/$',
                           'ticket_list'),
                       url(r'^ticket/detail/(?P<ticket_id>\d+)/$',
                           'ticket_detail'),
                       url(r'^faq/$',
                           'faq'),
                       url(r'^staff/$',
                           'support_staff'),
                       url(r'^ticket/resolve/(?P<ticket_id>\d+)/$',
                           'ticket_resolve'),
                       url(r'^invitation/list/$',
                           'invitation_list'),
                       url(r'^guide/$',
                           'guide'),
                       url(r'^passreset/$',
                           auth_views.password_reset,
                           {'template_name': 'password_reset_form.html'}),
                       url(r'^passresetdone/$',
                           auth_views.password_reset_done,
                           {'template_name': 'password_reset_done.html'}),
                       url(r'^passresetconfirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',
                           auth_views.password_reset_confirm,
                           {'template_name': 'password_reset_confirm.html'}),
                       url(r'^passresetcomplete/$',
                           auth_views.password_reset_complete,
                           {'template_name': 'password_reset_complete.html'}),
                       )
