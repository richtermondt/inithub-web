'''

@author: rtermondt
'''
from support.models import Ticket, Item, Item_Type

from django.contrib import admin


class TicketAdmin(admin.ModelAdmin):
    list_display = ('short_desc',)
    fields = ('short_desc', 'comment')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('comment',)


class Item_TypeAdmin(admin.ModelAdmin):
    list_display = ('short_desc',)

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Item_Type, Item_TypeAdmin)
