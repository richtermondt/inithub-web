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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from support.models import TicketForm, ItemForm, Ticket, Item
from manager.models import Invitation, Profile
from manager.constants import RECORDS_PER_PAGE, SUPPORT_TICKET_NEW_EVENT,\
    SUPPORT_TICKET_REPLY
from datetime import datetime
from manager.utils import queue_email, queue_internal_email_alert
from django.template.loader import get_template
from django.template import Context
from manager.constants import ACCESS_REQUEST_APPROVED_EVENT, ACCESS_REQUEST_APPROVED_SUBJECT, SUPPORT_TICKET_CUSTOMER_REPLY


@login_required()
def ticket_new(request):
    system_message = None
    if request.POST:
        form = TicketForm(request.POST)
        if form.is_valid():
            profile_id = request.session['profile_id']
            comment = form.cleaned_data['comment']
            short_desc = form.cleaned_data['short_desc']
            Ticket.objects.create(profile_id=profile_id,
                                  short_desc=short_desc, comment=comment)
            queue_internal_email_alert(
                short_desc, comment, SUPPORT_TICKET_NEW_EVENT)
            system_message = 'Support request submitted'
        else:
            system_message = 'Error'
    else:
        form = TicketForm()

    return render_to_response('support_ticket_new.html', {
        'system_message': system_message,
        'form': form,
    }, context_instance=RequestContext(request))


@login_required()
def ticket_list(request):
    system_message = None
    profile_id = request.session['profile_id']
    tickets = Ticket.objects.filter(
        profile_id=profile_id).order_by('create_date').reverse()
    return render_to_response('support_list.html', {
        'system_message': system_message,
        'my_tickets': tickets,
    }, context_instance=RequestContext(request))


@login_required()
def guide(request):
    system_message = None
    new_user = False
    if 'new_user' in request.GET:
        qs_user = request.GET['new_user']
        if qs_user == 'true':
            new_user = True
    return render_to_response('guide.html', {
        'new_user': new_user,
        'system_message': system_message,
    }, context_instance=RequestContext(request))


@login_required()
def ticket_detail(request, ticket_id):
    system_message = None
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        profile = ticket.profile
        ticket_items = Item.objects.filter(ticket_id=ticket_id).values(
            'id',
            'comment',
            'create_date',
            'profile__first_name',
            'profile__last_name').order_by('create_date').reverse()
    except Ticket.DoesNotExist:
        system_message = 'Ticket does not exist.'
        ticket = None
    return render_to_response('support_ticket_detail.html', {
        'system_message': system_message,
        'ticket': ticket,
        'profile': profile,
        'ticket_items': ticket_items,
    }, context_instance=RequestContext(request))


@login_required()
def faq(request):
    return render_to_response('faq.html', {
        'system_message': 'Hello world!',
    }, context_instance=RequestContext(request))


@login_required()
def item_new(request, ticket_id=None):
    system_message = None
    if request.POST:
        ticket_id = request.POST['ticket_id']
        profile_id = request.session['profile_id']
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket_profile_id = ticket.profile_id
        subject = 'RE: ' + ticket.short_desc
        item_type_id = 1  # hard code to 1= internal
        form = ItemForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            Item.objects.create(ticket_id=ticket_id, profile_id=profile_id,
                                item_type_id=item_type_id, comment=comment)
            if profile_id == ticket_profile_id:
                # response from customer
                queue_internal_email_alert(
                    subject,
                    comment,
                    SUPPORT_TICKET_CUSTOMER_REPLY)
            else:
                # reply from staff, send email to customer
                profile = Profile.objects.get(pk=ticket_profile_id)
                email = profile.email
                plaintext = get_template('email/support_response.txt')
                d = Context({'first_name': profile.first_name, 'ticket_id':
                             ticket_id, 'comment': comment})
                text_content = plaintext.render(d)
                queue_email(subject, text_content, email, SUPPORT_TICKET_REPLY)
            system_message = "Reply added"
            return ticket_detail(request, ticket_id)

        else:
            system_message = 'Error'
            return render_to_response('support_item_new.html', {
                                      'system_message': system_message,
                                      'ticket_id': ticket_id,
                                      'form': form,
                                      }, context_instance=RequestContext(request))

    else:
        form = ItemForm()

        return render_to_response('support_item_new.html', {
                                  'system_message': system_message,
                                  'ticket_id': ticket_id,
                                  'form': form,
                                  }, context_instance=RequestContext(request))


@login_required()
def support_staff(request):
    system_message = None
    if request.user.is_staff:
        if request.POST:
            search_field = request.POST.get('search_field', 'none')
            search_value = request.POST['search_text']
            if search_field == 'ticket_id':
                ticket_list = Ticket.objects.filter(
                    id=search_value).order_by('create_date')
            elif search_field == 'keyword':
                ticket_list = Ticket.objects.filter(Q(comment__contains=search_value) | Q(
                    short_desc__contains=search_value)).order_by('create_date')
        else:
            ticket_list = Ticket.objects.filter(
                is_resolved=False).order_by('create_date')

        paginator = Paginator(ticket_list, RECORDS_PER_PAGE)
        page = request.GET.get('page')
        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            tickets = paginator.page(1)
        except EmptyPage:
            tickets = paginator.page(paginator.num_pages)
        return render_to_response('support_staff.html', {
                                  'system_message': system_message,
                                  'my_tickets': tickets,
                                  }, context_instance=RequestContext(request))
    else:
        system_message = 'Invalid request'
        return render_to_response('system.html', {
                                  'system_message': system_message,
                                  }, context_instance=RequestContext(request))


@login_required()
def ticket_resolve(request, ticket_id=None):
    system_message = None
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket.is_resolved = True
        ticket.save()
        system_message = 'Ticket resolved!'
    except Ticket.DoesNotExist:
        system_message = 'Ticket does not exist.'
        ticket = None
    return render_to_response('support_ticket_resolve.html', {
        'system_message': system_message,
    }, context_instance=RequestContext(request))


@login_required()
def invitation_list(request):
    system_message = None
    if request.POST:
        if 'invitation' in request.POST:
            invitations = request.POST.getlist('invitation')
            for invitation in invitations:
                invite = Invitation.objects.get(id=invitation)
                invite.approved_date = datetime.now()
                invite.save()
                plaintext = get_template('email/create_profile.txt')
                d = Context({'uid': invite.signup_key})
                text_content = plaintext.render(d)
                queue_email(
                    ACCESS_REQUEST_APPROVED_SUBJECT,
                    text_content,
                    invite.email,
                    ACCESS_REQUEST_APPROVED_EVENT)
            system_message = 'Access request(s) approved!'

    invitation_list = Invitation.objects.filter(approved_date=None)
    paginator = Paginator(invitation_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        invitations = paginator.page(page)
    except PageNotAnInteger:
        invitations = paginator.page(1)
    except EmptyPage:
        invitations = paginator.page(paginator.num_pages)

    return render_to_response('invitation_list.html', {
                              'system_message': system_message,
                              'invitations': invitations
                              }, context_instance=RequestContext(request))


@login_required()
def ticket_search(request):
    system_message = None
    return render_to_response('support_search.html', {
                              'system_message': system_message,
                              }, context_instance=RequestContext(request))
