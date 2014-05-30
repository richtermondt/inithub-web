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
from manager.models import Initiative_Service, Initiative_Service_Offer, Milestones


def initiative_service_needed():
    return Initiative_Service.objects.filter(
        initiative__is_public=True
    ).values(
        'initiative__short_desc',
        'initiative__uuid',
        'service__short_desc',
        'create_date'
    ).order_by('-create_date')


def initiative_service_contibutions():
    return Initiative_Service_Offer.objects.filter(
        initiative__is_public=True, is_accepted=True
    ).values(
        'initiative__short_desc',
        'service__short_desc',
        'profile__first_name',
        'profile__last_name',
        'create_date',
        'initiative__uuid'
    ).order_by('-create_date')


def milestone_targets():
    return Milestones.objects.filter(
        initiative__is_public=True,
        target_date__isnull=False).values(
        'initiative__short_desc',
        'milestone__short_desc',
        'target_date',
        'initiative__uuid').order_by('-target_date')


def milestone_completed():
    return Milestones.objects.filter(
        initiative__is_public=True,
        complete_date__isnull=False).values(
        'initiative__short_desc',
        'milestone__short_desc',
        'complete_date',
        'initiative__uuid').order_by('-complete_date')
