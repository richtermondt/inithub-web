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
from manager.models import Subject, Initiative, Message
from manager.dao import initiative_dao


def subject_create(
        initiative_id,
        profile_id,
        short_desc,
        long_desc,
        is_public):
    Subject.objects.create(
        initiative_id=initiative_id,
        profile_id=profile_id,
        short_desc=short_desc,
        long_desc=long_desc,
        is_public=True
    )


def subjects_by_initiative(profile_id):
    initiative_id_list = initiative_dao.all_contributing_initiative_ids(
        profile_id)
    subjects = Initiative.objects.filter(
        id__in=initiative_id_list).values(
        'uuid',
        'short_desc',
        'subject__id',
        'subject__short_desc').order_by('subject__short_desc')
    return subjects


def subject_messages(subject_id):
    return Message.objects.filter(subject_id=subject_id).values(
        'id',
        'profile_id',
        'comment',
        'create_date',
        'profile__first_name',
        'profile__last_name',
    ).order_by('-create_date')


def subject_by_id(subject_id):
    return Subject.objects.get(pk=subject_id)


def message_create(subject_id, profile_id, comment):
    return Message.objects.create(
        subject_id=subject_id,
        profile_id=profile_id,
        comment=comment)
