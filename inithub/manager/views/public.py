'''

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
