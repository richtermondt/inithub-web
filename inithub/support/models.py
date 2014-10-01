'''

@author: rtermondt
'''
from django.db import models
from django.forms import ModelForm
from django.forms import CharField

# Create your models here.


class Message_Queue(models.Model):
    event = models.CharField(max_length=50)
    event_table = models.CharField(max_length=100)
    event_ref = models.IntegerField(null=True)
    deliver_to = models.CharField(max_length=100)
    message_subject = models.CharField(max_length=100)
    message_body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    sent_date = models.DateTimeField(null=True, blank=True, default=None)


class Message_Queue_Error(models.Model):
    message_queue = models.ForeignKey(Message_Queue)
    error_text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    profile = models.ForeignKey('manager.Profile', editable=False)
    short_desc = models.CharField(max_length=45)
    comment = models.TextField()
    is_resolved = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class TicketForm(ModelForm):
    short_desc = CharField(label='Subject')

    class Meta:
        model = Ticket
        exclude = ['is_resolved']


class Item_Type(models.Model):
    short_desc = models.CharField(max_length=25)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Item(models.Model):
    profile = models.ForeignKey('manager.Profile', editable=False)
    ticket = models.ForeignKey(Ticket, editable=False)
    item_type = models.ForeignKey(Item_Type, editable=False)
    comment = models.TextField()
    is_solution = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class ItemForm(ModelForm):

    class Meta:
        model = Item
        exclude = ['is_solution']
