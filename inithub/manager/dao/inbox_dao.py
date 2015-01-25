'''

@author: rtermondt
'''

from manager.models import Initiative_Service_Offer


def get_inbox_offer_count(profile_id):
    offer_list = Initiative_Service_Offer.objects.filter(
        initiative__profile_id=profile_id,
        is_accepted=False).values(
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
        is_accepted=False).values(
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
