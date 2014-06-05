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
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from manager.forms import ProfileForm, \
    PasswordChangeForm, ProfileCreateForm
from manager.models import Profile, Invitation, Services, Initiative, \
    Initiative_Service_Offer, Profile_Rating, Subscription, Subscription_Profile
from django.template.loader import get_template
from django.template import Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
import uuid
from manager.utils import queue_email
from manager.constants import PROFILE_CREATE_EVENT, CONFIRM_ACCOUNT_SUBJECT,\
    ACCOUNT_CONFIRMED_SUBJECT, ACCOUNT_CONFIRMED_EVENT, RECORDS_PER_PAGE
from inithub import settings


@login_required()
def profile_manager(request):
    system_message = None
    if request.POST:
        form = ProfileForm(request.POST)
        if form.is_valid() == False:
            system_message = "Error"
        else:
            try:
                email = form.cleaned_data['email']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                zip_code = form.cleaned_data['zip']
                p = Profile.objects.get(pk=request.session['profile_id'])
                p.first_name = form.cleaned_data['first_name']
                p.last_name = form.cleaned_data['last_name']
                p.email = email
                p.city = city
                p.state = state
                p.zip = zip_code
                p.save()
                user = p.user
                user.username = email
                user.email = email
                user.save()
                system_message = 'Profile updated'
            except IntegrityError:
                system_message = 'Email not unique'
            except Profile.DoesNotExist:
                return render_to_response('system.html', {
                                          'system_message': 'An error occurred processing your request.',
                                          }, context_instance=RequestContext(request))
    else:
        p = Profile.objects.get(pk=request.session['profile_id'])
        form = ProfileForm(initial={
                           'first_name': p.first_name,
                           'last_name': p.last_name,
                           'email': p.email,
                           'city': p.city,
                           'state': p.state,
                           'zip': p.zip,
                           })
    return render_to_response('profile_manager.html', {
                              'system_message': system_message,
                              'profile': p,
                              'form': form,
                              }, RequestContext(request))

        
def profile_create(request, invite_key=None):
    invite = getattr(settings, 'INVITATION_SYSTEM', None)
    if invite == None or invite == False:
        form = ProfileCreateForm()
        return render_to_response('create_profile.html', {
                                  'system_message': None,
                                  'form': form,
                                  }, context_instance=RequestContext(request))
        
    try:
        invite = Invitation.objects.get(signup_key=invite_key)
        if invite.profile_id is not None:
            return render_to_response('system.html', {
                                      'system_message': 'Invite Key already associated with a profile.',
                                      'top_menu': 'landing',
                                      }, context_instance=RequestContext(request))
        else:
            if invite.approved_date is None:
                return render_to_response('system.html', {
                                          'system_message': 'Invitation has not been approved.',
                                          'top_menu': 'landing',
                                          }, context_instance=RequestContext(request))
            form = ProfileCreateForm()
            return render_to_response('create_profile.html', {
                                      'system_message': None,
                                      'form': form,
                                      'invite_key': invite_key
                                      }, context_instance=RequestContext(request))
    except Invitation.DoesNotExist:
        return render_to_response('system.html', {
                                  'system_message': 'Invite Key not recognized.',
                                  }, context_instance=RequestContext(request))


def profile_add(request):
    if request.POST:
        system_message = None
        form = ProfileCreateForm(request.POST)
        terms = request.POST.getlist('agree')
        if len(terms) != 1:
            system_message = 'You must agree to our Terms of Service'
        else:

            if form.is_valid() == False:
                system_message = 'Form error'
            else:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    system_message = 'Passwords must be the same'
                else:
                    try:
                        test_profile = Profile.objects.get(email=email)
                        system_message = 'Email already exists.'
                    except Profile.DoesNotExist:
                        User.objects.create_user(email, email, password1)
                        #p = Profile.objects.create(first_name=first_name, last_name=last_name, email=email)
                        user = authenticate(username=email, password=password1)
                        login(request, user)
                        uid = uuid.uuid4()
                        user_profile = user.get_profile()
                        request.session['profile_id'] = user_profile.id
                        user_profile.first_name = first_name
                        user_profile.last_name = last_name
                        user_profile.email = email
                        user_profile.confirm_key = uid
                        user_profile.save()
                        plaintext = get_template('email/confirm.txt')
                        d = Context({'first_name': first_name, 'uid': uid})
                        text_content = plaintext.render(d)
                        queue_email(
                            CONFIRM_ACCOUNT_SUBJECT,
                            text_content,
                            email,
                            PROFILE_CREATE_EVENT)
                        if 'invite_key' in request.POST:
                            invite_key = request.POST['invite_key']
                            invite = Invitation.objects.get(
                                signup_key=invite_key)
                            invite.profile_id = user_profile.id
                            invite.save()

                        return HttpResponseRedirect(
                            '/support/guide/?new_user=true')
    else:
        form = ProfileCreateForm()
        system_message = 'invalid request'

    return render_to_response('create_profile.html', {
                              'system_message': system_message,
                              'form': form
                              }, context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return render_to_response('system.html', {
                              'system_message': "Your session has expired",
                              'top_menu': 'landing'
                              }, context_instance=RequestContext(request))


@login_required()
def my_password_change(request):
    system_message = None
    if request.POST:
        form = PasswordChangeForm(request.POST)
        if form.is_valid() == False:
            system_message = 'Form validation error'
        else:
            curr_pass = request.POST['current_password']
            user = request.user
            if user.check_password(curr_pass):
                pass1 = request.POST['new_password1']
                pass2 = request.POST['new_password2']
                if pass1 == pass2:
                    user.set_password(pass1)
                    user.save()
                    system_message = 'Password updated.'
                else:
                    system_message = 'New passwords are not the same.'
            else:
                system_message = 'Current password is incorrect.'

    form = PasswordChangeForm()
    return render_to_response('password_change.html', {
                              'system_message': system_message,
                              'form': form,
                              }, context_instance=RequestContext(request))


@login_required()
def profile_view_ratings(request, uuid):
    p = Profile.objects.get(confirm_key=uuid)
    rating_list = Profile_Rating.objects.filter(profile_id=p.id)
    num_ratings = rating_list.count()
    average_rating = rating_list.aggregate(Avg('rating')).values()[0]

    paginator = Paginator(rating_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        rating = paginator.page(page)
    except PageNotAnInteger:
        rating = paginator.page(1)
    except EmptyPage:
        rating = paginator.page(paginator.num_pages)

    return render_to_response('profile_view_ratings.html', {
                              'profile': p,
                              'num_ratings': num_ratings,
                              'rating_list': rating,
                              'average_rating': average_rating
                              }, RequestContext(request))


@login_required()
def profile_view(request, uuid):
    my_profile_id = request.session['profile_id']
    profile_id = Profile.objects.get(confirm_key=uuid).id
    service_selected = Services.objects.filter(
        profile_id=profile_id).values('service__short_desc')
    initiatives = Initiative.objects.filter(
        profile_id=profile_id, is_public=True)
    services_contrib = Initiative_Service_Offer.objects.filter(
        profile_id=profile_id,
        is_accepted=True).values(
        'service__short_desc',
        'initiative__short_desc',
    )
    p = Profile.objects.get(pk=profile_id)

    rating = Profile_Rating.objects.filter(profile_id=profile_id)
    num_ratings = rating.count()
    average_rating = rating.aggregate(Avg('rating')).values()[0]
    # cannot rate yourself
    try:
        if int(my_profile_id) == int(profile_id):
            haveWorkedTogether = False
        else:
            haveWorkedTogether = checkProfilesHaveWorkedTogether(
                profile_id, my_profile_id)
    except TypeError:
        return render_to_response('system.html', {
                                  'system_message': 'An error occurred processing your request.',
                                  }, context_instance=RequestContext(request))

    return render_to_response('profile_view.html', {
                              'profile': p,
                              'service_selected': service_selected,
                              'initiatives': initiatives,
                              'num_ratings': num_ratings,
                              'services_contrib': services_contrib,
                              'haveWorkedTogether': haveWorkedTogether,
                              'rating': average_rating
                              }, RequestContext(request))


def checkProfilesHaveWorkedTogether(profile_id1, profile_id2):
    retval = False
    profile_id1_list = []
    profile_id2_list = []

    int1 = Initiative.objects.filter(profile_id=profile_id1, is_public=True)
    for initiative in int1:
        profile_id1_list.append(initiative.pk)

    int2 = Initiative.objects.filter(profile_id=profile_id2, is_public=True)
    for initiative in int2:
        profile_id2_list.append(initiative.pk)

    services_contrib1 = Initiative_Service_Offer.objects.filter(
        profile_id=profile_id1, is_accepted=True)
    for service in services_contrib1:
        profile_id1_list.append(service.initiative_id)

    services_contrib2 = Initiative_Service_Offer.objects.filter(
        profile_id=profile_id2, is_accepted=True)
    for service in services_contrib2:
        profile_id2_list.append(service.initiative_id)

    profile_id1_set = set(profile_id1_list)
    profile_id2_set = set(profile_id2_list)

    for initiative_id in profile_id1_set:
        print(initiative_id)
        if initiative_id in profile_id2_set:
            retval = True
            break
    return retval


@login_required()
def profile_rate(request, uuid=None):
    system_message = None
    my_profile_id = request.session['profile_id']
    if request.POST:
        uuid = request.POST['uuid']
        profile_id = Profile.objects.get(confirm_key=uuid).id
        if 'star' in request.POST:
            rating = Decimal(request.POST['star'])
        else:
            system_message = "Error, you must select a rating."
            if 'profile_rating_id' in request.POST:
                profile_rating = Profile_Rating.objects.get(
                    pk=request.POST['profile_rating_id'])
            else:
                profile_rating = None

            return render_to_response('profile_rate.html', {
                                      'system_message': system_message,
                                      'profile_id': profile_id,
                                      'profile_rating': profile_rating,
                                      }, RequestContext(request))

        comments = request.POST['comments']
        if 'profile_rating_id' in request.POST:
            profile_rating_id = request.POST['profile_rating_id']
            system_message = "Your rating has been updated"
            profile_rating = Profile_Rating.objects.get(pk=profile_rating_id)
            profile_rating.rating = rating
            profile_rating.comments = comments
            profile_rating.save()
        else:
            system_message = "Your rating has been added"
            profile_rating = Profile_Rating.objects.create(
                profile_id=profile_id,
                profile_reviewer_id=my_profile_id,
                rating=rating,
                comments=comments
            )
    else:
        try:
            profile_rating = Profile_Rating.objects.get(
                profile_id=Profile.objects.get(
                    confirm_key=uuid).id,
                profile_reviewer_id=my_profile_id)
            system_message = "Update rating"
        except Profile_Rating.DoesNotExist:
            profile_rating = None

    return render_to_response('profile_rate.html', {
                              'system_message': system_message,
                              'uuid': uuid,
                              'profile_rating': profile_rating,
                              }, RequestContext(request))


def email_confirm(request, confirm_key):
    try:
        p = Profile.objects.get(confirm_key=confirm_key)
        if p.is_confirmed:
            return render_to_response('system.html', {
                                      'system_message': 'Your account has already been confirmed.',
                                      }, context_instance=RequestContext(request))
        else:
            p.is_confirmed = True
            p.save()
            plaintext = get_template('email/confirmed.txt')
            d = Context({'first_name': p.first_name})
            text_content = plaintext.render(d)
            queue_email(ACCOUNT_CONFIRMED_SUBJECT,
                        text_content, p.email, ACCOUNT_CONFIRMED_EVENT)
            return render_to_response('system.html', {
                                      'system_message': 'Thank you, your account has been confirmed.',
                                      }, context_instance=RequestContext(request))
    except Profile.DoesNotExist:
        return render_to_response('system.html', {
                                  'system_message': 'Confirm Key not recognized.',
                                  }, context_instance=RequestContext(request))


@login_required()
def subscription_manager(request):
    system_message = None
    profile_id = request.session['profile_id']
    if request.POST:
        Subscription_Profile.objects.filter(profile_id=profile_id).delete()
        if 'subscriptions' in request.POST:
            subscriptions = request.POST['subscriptions']
            for subscription in subscriptions:
                Subscription_Profile.objects.create(
                    profile_id=profile_id,
                    subscription_id=subscription)
        system_message = 'Subscriptions updated'

    subscriptions = Subscription.objects.all()
    my_subs = Subscription_Profile.objects.filter(profile_id=profile_id)
    return render_to_response('subscription_manager.html', {
                              'system_message': system_message,
                              'subscriptions': subscriptions,
                              'my_subs': my_subs
                              }, context_instance=RequestContext(request))
