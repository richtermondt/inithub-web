'''
Copyright 2012-2014 Rich Termondt

This file is part of Inithub-web.

Inithub-web is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Inithub-web is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Inithub-web.  If not, see <http://www.gnu.org/licenses/>.

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
