'''

@author: rtermondt
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template
from django.db import IntegrityError
from django.db import transaction
from manager.forms import SubjectAddForm, MessageAddForm
from manager.dao import initiative_dao
from manager.dao import subject_dao
from manager.models import Profile_Invite, Invitation, Promotion, Profile
from manager.utils import queue_email
from manager.constants import USER_INVITE_SUBJECT, USER_INVITE_EVENT
from manager.forms import UserInviteForm
import uuid
from datetime import datetime

#from manager import utils
#from datetime import datetime


@login_required()
def collaboration(request):
    system_message = None
    return render_to_response('collaboration.html', {
                              'system_message': system_message
                              }, context_instance=RequestContext(request))


@login_required()
def subject_add(request, initiative_uuid=None):
    system_message = None
    profile_id = request.session['profile_id']
    if request.POST:
        form = SubjectAddForm(request.POST)
        if form.is_valid() == False:
            system_message = 'Error!'
        else:
            if 'initiative_uuid' in request.POST:
                uuid = request.POST['initiative_uuid']
                if uuid != "":
                    initiative_id = initiative_dao.get_pulic_intitiative_id(
                        uuid)
                    # defensive check - make sure submitter id contributor
                    contrib_init = initiative_dao.all_contributing_initiative_ids(
                        profile_id)
                    can_create_subject = False
                    for init_id in contrib_init:
                        if init_id == int(initiative_id):
                            can_create_subject = True
                            break
                    if not can_create_subject:
                        system_message = 'Error! You must be Initiative contributor or sponsor to create subject.'
                    else:
                        short_desc = form.cleaned_data['short_desc']
                        long_desc = form.cleaned_data['long_desc']
                        subject_dao.subject_create(
                            initiative_id,
                            profile_id,
                            short_desc,
                            long_desc,
                            True)
                        system_message = "Subject successfully created."
                        form = SubjectAddForm()
                else:
                    system_message = 'Error! Initiative is required.'
            else:
                system_message = 'Error! Initiative missing'
    else:
        form = SubjectAddForm()

    if initiative_uuid is None:
        #initiatives = initiative_dao.initiative_list_by_profile_id(profile_id)
        initiatives = initiative_dao.all_contributing_initiatives(profile_id)

    else:
        initiatives = None

    return render_to_response('subject_add.html', {
                              'system_message': system_message,
                              'form': form,
                              'initiatives': initiatives,
                              'initiative_uuid': initiative_uuid
                              }, context_instance=RequestContext(request))


@login_required()
def subject_list(request):
    system_message = None
    profile_id = request.session['profile_id']
    subjects = subject_dao.subjects_by_initiative(profile_id)
    return render_to_response('subject_list.html', {
                              'system_message': system_message,
                              'subjects': subjects
                              }, context_instance=RequestContext(request))


@login_required()
def subject_messages(request, subject_id=None):
    system_message = None
    if request.POST:
        form = MessageAddForm(request.POST)
        if form.is_valid() == False:
            system_message = 'Error!'
        else:
            comment = form.cleaned_data['comment']
            profile_id = request.session['profile_id']
            subject_id = request.POST['subject_id']
            subject_dao.message_create(subject_id, profile_id, comment)
            form = MessageAddForm()
    else:
        form = MessageAddForm()
    #lastUpdate = datetime.now()
    #newDT = lastUpdate.strftime('%B %d, %Y, %I:%M %p')
    messages = subject_dao.subject_messages(subject_id)
    subject = subject_dao.subject_by_id(subject_id)
    return render_to_response('subject_messages.html', {
                              'system_message': system_message,
                              'messages': messages,
                              'form': form,
                              'subject': subject,
                              #'last_update': newDT
                              }, context_instance=RequestContext(request))


@login_required()
def invite(request):
    system_message = None
    profile_id = request.session['profile_id']
    max_invitations = 5
    existing_invites = Profile_Invite.objects.filter(profile_id=profile_id)
    invites_remaining = max_invitations - existing_invites.count()

    if invites_remaining <= 0:
        system_message = "You have used all invites."
    else:
        if request.POST:
            post_form = UserInviteForm(request.POST)
            if post_form.is_valid():
                email = request.POST['email']
                message = request.POST['message']
                uid = uuid.uuid4()
                promotion = 'USER'
                p = Promotion.objects.get(code=promotion)
                promotion_id = p.pk
                p = Profile.objects.get(pk=profile_id)

                try:
                    with transaction.commit_on_success():
                        new_invite = Invitation.objects.create(
                            email=email,
                            signup_key=uid,
                            promotion_id=promotion_id,
                            approved_date=datetime.now())
                        Profile_Invite.objects.create(
                            profile_id=profile_id,
                            invitation_id=new_invite.pk,
                            message=message)
                        plaintext = get_template(
                            'email/create_profile_invite.txt')
                        d = Context({'uid': new_invite.signup_key,
                                     'message': message,
                                     'first_name': p.first_name,
                                     'last_name': p.last_name})
                        text_content = plaintext.render(d)
                        queue_email(
                            USER_INVITE_SUBJECT,
                            text_content,
                            new_invite.email,
                            USER_INVITE_EVENT)
                        system_message = 'Invitation successfully created!'
                        invites_remaining = invites_remaining - 1
                except IntegrityError:
                    system_message = "Email already exists."
            else:
                system_message = "Form validation error."

    form = UserInviteForm()
    return render_to_response('collaboration_invite.html', {
                              'system_message': system_message,
                              'max_invitations': max_invitations,
                              'invites_remaining': invites_remaining,
                              'form': form
                              }, context_instance=RequestContext(request))
