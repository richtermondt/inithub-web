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
from manager.models import Profile, Interest, Service, Promotion, Invitation, Milestone, Subscription

from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name')


class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('short_desc',)


class InterestAdmin(admin.ModelAdmin):
    list_display = ('short_desc',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('short_desc',)


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('short_desc',)


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('short_desc',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
