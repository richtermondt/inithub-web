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

The copyright holder(s) may consider permitting uses outside of the license terms on a case-by-case basis

@author: rtermondt
'''
from inithub import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from manager.forms import InvitationForm, SigninForm, ProfileCreateForm
from manager.models import Profile, Invitation, Promotion
import uuid
from django.db import IntegrityError
from manager.utils import queue_internal_email_alert
from manager.dao import inbox_dao
import logging
from manager.constants import INTERNAL_INVITATION_REQUEST_BODY, INTERNAL_INVITATION_REQUEST_SUBJECT, INVITATION_EVENT

log = logging.getLogger(__name__)


def about(request):
    if settings.INVITATION_SYSTEM == True:
        form = InvitationForm()
    else: 
        form = ProfileCreateForm()
        
    return render_to_response('landing.html', {
                              'system_message': None,
                              'form': form,
                              }, context_instance=RequestContext(request))


def signin(request):
    system_message = None
    if request.POST:
        form = SigninForm(request.POST)
        if form.is_valid() == False:
            system_message = 'Authentication failed. Please try again.'
        else:
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    try:
                        p = Profile.objects.get(email=email)
                        request.session['profile_id'] = p.pk
                        msgs = inbox_dao.get_inbox_offer_count(p.pk)
                        if msgs == 0:
                            return HttpResponseRedirect('/manager/news/')
                        else:
                            return HttpResponseRedirect('/manager/inbox/')

                    except Profile.DoesNotExist:
                        system_message = 'Authentication failed. Please try again.'
                        log.warn(system_message)
                else:
                    # Return a 'disabled account' error message
                    return render_to_response(
                        'system.html', {
                            'system_message': 'Account disabled.', }, context_instance=RequestContext(request))
            else:
                # Return an 'invalid login' error message.
                system_message = "Authentication failed. Please try again."
                log.warn(system_message)
                form = SigninForm()

    # always reset form if we make it this far
    form = SigninForm()
    return render_to_response('login.html', {
                              'system_message': system_message,
                              'form': form,
                              }, context_instance=RequestContext(request))


def invitation(request):
    system_message = None
    if request.POST:
        form = InvitationForm(request.POST)
        if form.is_valid() == False:
            system_message = "Error"
        else:
            email = form.cleaned_data['email']
            if not request.POST.get('promotion', ''):
                promotion = 'INNOHUB'
            else:
                promotion = request.POST['promotion']

            p = Promotion.objects.get(code=promotion)
            promotion_id = p.pk
            uid = uuid.uuid4()
            try:
                Invitation.objects.create(
                    email=email,
                    signup_key=uid,
                    promotion_id=promotion_id)
                queue_internal_email_alert(
                    INTERNAL_INVITATION_REQUEST_SUBJECT,
                    INTERNAL_INVITATION_REQUEST_BODY,
                    INVITATION_EVENT)
                #system_message = 'Thank you! We will notify you when your request has been processed.'
                return HttpResponseRedirect('/manager/invitation/success/')
                '''
                return render_to_response('system.html', {
                    'system_message': system_message,
                    'top_menu': 'landing'
                }, context_instance=RequestContext(request))
                '''
            except IntegrityError:
                system_message = "Email already exists."
                log.warn(system_message)
                form = InvitationForm()
    else:
        form = InvitationForm()

    return render_to_response('invitation.html', {
                              'system_message': system_message,
                              'form': form,
                              }, context_instance=RequestContext(request))
