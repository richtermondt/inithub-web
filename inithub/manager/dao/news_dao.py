'''

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
