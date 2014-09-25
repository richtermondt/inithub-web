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
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from manager.resources import InitiativeResource, ApiTokenResource, UserResource, SubjectResource, MessageResource, ProfileResource, WebMessageResource
from axes.decorators import watch_login
from manager.views import signin, about, invitation
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
initiative_resource = InitiativeResource()
user_resource = UserResource()
token_resource = ApiTokenResource()
subject_resource = SubjectResource()
message_resource = MessageResource()
profile_resource = ProfileResource()
web_message_resource = WebMessageResource()

# public urls
urlpatterns = patterns('manager.views',
                       url(r'^signin/$',
                           watch_login(signin)),
                       url(r'^about/$',
                           about),
                       url(r'^invitation/$',
                           invitation),
                       url(r'^invitation/success/$',
                           TemplateView.as_view(template_name="thank_you.html")),
                       )
invite = getattr(settings, 'INVITATION_SYSTEM', None)
if invite == True:
    urlpatterns += patterns('manager.views',
                        url(r'^profile/create/(?P<invite_key>.+)/$',
                            'profile_create'),
                        )
else:
        urlpatterns += patterns('manager.views',
                        url(r'^profile/create/$',
                            'profile_create'),
                        )
        
urlpatterns += patterns('manager.views',
                        url(r'^profile/add/$', 'profile_add'),
                        #url(r'^signin/$', 'signin'),
                        #url(r'^about/$', 'about'),
                        #url(r'^invitation/$', 'invitation'),
                        # match any character
                        url(r'^profile/confirm/(?P<confirm_key>.+)/$',
                            'email_confirm'),
                        # match only alpha/numeric
                        #url(r'^signin/(?P<invite_key>\w+)/$', 'manager.views.profile_create'),
                        url(r'^profile/manager/$', 'profile_manager'),
                        url(r'^profile/service/$', 'service_manager'),
                        url(r'^profile/interest/$', 'interest_manager'),
                        url(r'^profile/subscription/$',
                            'subscription_manager'),
                        url(r'^logout/$', 'logout_view'),
                        url(r'^profile/password/change/$',
                            'my_password_change'),
                        url(
                            r'^profile/view/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                            'profile_view'),
                        url(
                            r'^profile/rate/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                            'profile_rate'),
                        url(
                            r'^profile/ratings/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',
                            'profile_view_ratings'),
                        url(r'^profile/rate/$', 'profile_rate'),
                        )

urlpatterns += patterns('manager.views',
                        url(r'^news/$', 'news'),
                        url(r'^news/milestone/targets/$',
                            'milesstone_targets'),
                        url(r'^news/milestone/completed/$',
                            'milesstone_completed'),
                        url(r'^news/initiative/started/$',
                            'initiative_started'),
                        url(r'^news/service/requested/$',
                            'services_requested'),
                        url(r'^news/service/contributed/$',
                            'services_contributed'),
                        )
# initiatice urls
urlpatterns += patterns('manager.views',
                        url(r'^initiatives/$', 'initiatives'),
                        url(r'^initiatives/personal/$', 'my_initiatives'),
                        url(r'^initiative/detail/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_detail'),
                        url(r'^initiative/add/$', "initiative_add"),
                        url(r'^initiative/edit/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_edit'),
                        url(r'^initiative/edit/$', "initiative_edit_save"),
                        url(r'^initiative/service/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_service'),
                        url(r'^initiative/service/$',
                            "initiative_service_add"),
                        url(r'^initiative/milestones/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_milestones'),
                        url(r'^initiative/milestones/$', "initiative_milestones_add"),
                        url(r'^initiative/milestones/target/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_milestone_date'),
                        url(r'^initiative/service/offer/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_service_offer'),
                        url(r'^initiative/service/offer/$', 'initiative_service_offer'),
                        url(r'^initiative/rate/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_rate'),
                        url(r'^initiative/rate/$', 'initiative_rate'),
                        url(r'^initiative/search/$', 'initiative_search'),
                        url(r'^initiative/auto/$', 'initiative_auto'),
                        url(r'^initiative/milestone/date/$', 'initiative_milestone_date'),
                        url(r'^initiative/ratings/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_view_rating'),
                        url(r'^initiative/contributors/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'initiative_contributors'),
                        url(r'^initiative/contributors/$', 'initiative_contributors'),
                        url(r'^initiative/contributors/offer/(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'contributor_offers'),
                        url(r'^initiative/contributors/offer/$',
                            'contributor_offers'),
                        url(r'^initiative/payment/$',
                            'initiative_payment'),
                        )

urlpatterns += patterns('manager.views',
                        url(r'^inbox/$', 'inbox'),
                        url(r'^offer/process/$', 'offer_process'),
                        )

urlpatterns += patterns('manager.views',
                        url(r'^collaboration/$', 'subject_list'),
                        url(r'^collaboration/subject/add/$', 'subject_add'),
                        url(r'^collaboration/subject/add/(?P<initiative_uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'subject_add'),
                        url(r'^collaboration/subject/list/$', 'subject_list'),
                        url(r'^collaboration/subject/messages/(?P<subject_id>\d+)/$',
                            'subject_messages'),
                        url(r'^collaboration/subject/messages/$',
                            'subject_messages'),
                        url(r'^collaboration/invite/$', 'invite'),
                        )

urlpatterns += patterns('',
                        url(r'^api/', include(initiative_resource.urls),),
                        url(r'^api/', include(user_resource.urls),),
                        url(r'^api/', include(token_resource.urls),),
                        url(r'^api/', include(subject_resource.urls),),
                        url(r'^api/', include(message_resource.urls),),
                        url(r'^api/', include(profile_resource.urls),),
                        url(r'^api/web/', include(web_message_resource.urls),),
                        )
