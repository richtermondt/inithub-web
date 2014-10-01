'''

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
