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

from manager.models import Initiative_Service_Offer


def get_inbox_offer_count(profile_id):
    offer_list = Initiative_Service_Offer.objects.filter(
        initiative__profile_id=profile_id,
        is_accepted=None).values(
        'id',
        'is_accepted',
        'profile_id',
        'service__short_desc',
        'profile__first_name',
        'profile__last_name',
        'initiative__id',
        'initiative__short_desc')
    return offer_list.count()


def get_offer_list(profile_id):
    offer_list = Initiative_Service_Offer.objects.filter(
        initiative__profile_id=profile_id,
        is_accepted=None).values(
        'id',
        'is_accepted',
        'create_date',
        'service__short_desc',
        'profile__first_name',
        'profile__last_name',
        'profile__confirm_key',
        'initiative__id',
        'initiative__short_desc')
    return offer_list


def get_offer_list_all():
    offer_list = Initiative_Service_Offer.objects.all().values(
        'id',
        'is_accepted',
        'profile_id',
        'service__short_desc',
        'profile__first_name',
        'profile__last_name',
        'initiative__id',
        'initiative__short_desc')
    return offer_list
