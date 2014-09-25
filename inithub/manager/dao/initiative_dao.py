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
from manager.models import Initiative, Initiative_Service_Offer


def initiative_list_by_profile_id(profile_id):
    return Initiative.objects.all().filter(profile_id=profile_id)


def all_contributing_initiative_ids(profile_id):
    initiative_id_list = []
    initiatives = Initiative.objects.filter(
        profile_id=profile_id, is_public=True)
    for initiative in initiatives:
        initiative_id_list.append(initiative.id)

    services_contrib = Initiative_Service_Offer.objects.filter(
        profile_id=profile_id, is_accepted=True)
    for service in services_contrib:
        initiative_id_list.append(service.initiative_id)

    return initiative_id_list


def all_contributing_initiatives(profile_id):
    return Initiative.objects.all().filter(
        id__in=all_contributing_initiative_ids(profile_id))


def get_pulic_intitiative_id(uuid):
    initiative = Initiative.objects.get(uuid=uuid, is_public=True)
    return initiative.id


def get_intitiative_id(uuid):
    initiative = Initiative.objects.get(uuid=uuid)
    return initiative.id
