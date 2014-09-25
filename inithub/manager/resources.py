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
from tastypie.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.exceptions import NotFound
from tastypie.authentication import BasicAuthentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.models import ApiKey
from datetime import datetime


from manager.models import Initiative, Subject, Profile, Message
from manager.dao import initiative_dao

from django.contrib.auth.models import User
import logging

log = logging.getLogger(__name__)


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth'
        excludes = ['email', 'password', 'is_active', 'is_staff',
                    'is_superuser']
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
            'user': ALL_WITH_RELATIONS,
        }
        # Add it here.
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class ApiTokenResource(ModelResource):

    class Meta:
        queryset = ApiKey.objects.all()
        resource_name = "token"
        include_resource_uri = False
        fields = ["key"]
        list_allowed_methods = []
        detail_allowed_methods = ["get"]
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()

    def obj_get(self, bundle, **kwargs):
        if kwargs["pk"] != "auth":
            raise NotImplementedError("Resource not found")

        user = bundle.request.user
        if not user.is_active:
            raise NotFound("User not active")

        try:
            api_key = ApiKey.objects.get(user=user)
            #api_key.key = None
            # api_key.save()
        except ApiKey.DoesNotExist:
            api_key = ApiKey.objects.create(user=user)

        return api_key


class ProfileResource(ModelResource):

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        excludes = ['email', 'password']
        authentication = ApiKeyAuthentication()


class InitiativeResource(ModelResource):

    class Meta:
        queryset = Initiative.objects.all()
        resource_name = 'initiatives'
        authentication = ApiKeyAuthentication()

    def obj_get_list(self, request=None, **kwargs):
        user = request.user
        if not user.is_active:
            raise NotFound("User not active")

        user_profile = user.get_profile()

        initiative_id_list = initiative_dao.all_contributing_initiative_ids(
            user_profile.id)

        initiative_list = Initiative.objects.filter(id__in=initiative_id_list)

        return initiative_list


class SubjectResource(ModelResource):
    profile = fields.ForeignKey(ProfileResource, 'profile')
    initiative = fields.ForeignKey(InitiativeResource, 'initiative')
    first_name = fields.CharField(attribute='profile__first_name')
    last_name = fields.CharField(attribute='profile__last_name')
    initiative_name = fields.CharField(attribute='initiative__short_desc')

    class Meta:
        queryset = Subject.objects.all()
        resource_name = 'subject'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = ApiKeyAuthentication()

    def obj_get_list(self, bundle, **kwargs):
        user = bundle.request.user
        if not user.is_active:
            raise NotFound("User not active")

        user_profile = user.get_profile()

        initiative_id_list = initiative_dao.all_contributing_initiative_ids(
            user_profile.id)
        #initiative_id = request.GET.get('initiative_id', '')
        subject_list = Subject.objects.filter(
            initiative_id__in=initiative_id_list, is_public=True)

        return subject_list


class MessageResource(ModelResource):
    profile = fields.ForeignKey(ProfileResource, 'profile')
    subject = fields.ForeignKey(SubjectResource, 'subject')
    first_name = fields.CharField(attribute='profile__first_name')
    last_name = fields.CharField(attribute='profile__last_name')
    subject_id = fields.CharField(attribute='subject__id')

    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def obj_get_list(self, bundle, **kwargs):
        subject_id = bundle.request.GET.get('subject_id', '')
        message_list = Message.objects.filter(
            subject_id=subject_id, is_deleted=False)

        return message_list

    def obj_create(self, bundle, request=None, **kwargs):
        user = bundle.request.user
        if not user.is_active:
            raise NotFound("User not active")

        user_profile = user.get_profile()
        comm = bundle.data['comment']
        subject_id = bundle.data['subject_id']
        bundle.obj = Message(comment=comm,
                             profile_id=user_profile.id, subject_id=subject_id)
        bundle.obj.save()
        return bundle


class WebMessageResource(ModelResource):
    profile = fields.ForeignKey(ProfileResource, 'profile')
    subject = fields.ForeignKey(SubjectResource, 'subject')
    first_name = fields.CharField(attribute='profile__first_name')
    last_name = fields.CharField(attribute='profile__last_name')
    subject_id = fields.CharField(attribute='subject__id')

    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True
        authorization = DjangoAuthorization()
        authorization = Authorization()

    def obj_get_list(self, bundle, **kwargs):
        subject_id = bundle.request.GET.get('subject_id', '')
        last_update = datetime.strptime(bundle.request.GET.get(
            'last_update', ''), '%B %d, %Y, %I:%M %p')
        # June 3, 2013, 4:48 p.m.
        # time data 'May 16, 2013, 4:57 p.m.' does not match format '%Y-%m-%d %H:%M:%S+0000'\n"
        #last_update = bundle.request.GET.get('last_update', '')
        message_list = Message.objects.filter(
            subject_id=subject_id,
            create_date__gte=last_update,
            is_deleted=False)

        return message_list
