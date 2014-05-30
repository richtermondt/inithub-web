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
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manager.models import Initiative
from manager.constants import RECORDS_PER_PAGE
from manager.dao import news_dao


@login_required()
def news(request):
    system_message = None
    init_service = news_dao.initiative_service_needed()[0:10]
    init_service_offer = news_dao.initiative_service_contibutions()[0:10]
    milestone_targets = news_dao.milestone_targets()[0:10]
    milestone_complete = news_dao.milestone_completed()[0:10]
    initiatives = initiatives_sponsor()[0:10]

    return render_to_response('news.html', {
                              'system_message': system_message,
                              'init_service': init_service,
                              'init_service_offer': init_service_offer,
                              'milestone_targets': milestone_targets,
                              'initiatives': initiatives,
                              'milestone_complete': milestone_complete,
                              }, RequestContext(request))


def milesstone_targets(request):
    milestone_targets_list = news_dao.milestone_targets()
    paginator = Paginator(milestone_targets_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        milestone_targets = paginator.page(page)
    except PageNotAnInteger:
        milestone_targets = paginator.page(1)
    except EmptyPage:
        milestone_targets = paginator.page(paginator.num_pages)
    return render_to_response('news.html', {
                              'system_message': None,
                              'milestone_targets': milestone_targets,
                              }, RequestContext(request))


def milesstone_completed(request):
    milestone_complete_list = news_dao.milestone_completed()
    paginator = Paginator(milestone_complete_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        milestone_complete = paginator.page(page)
    except PageNotAnInteger:
        milestone_complete = paginator.page(1)
    except EmptyPage:
        milestone_complete = paginator.page(paginator.num_pages)
    return render_to_response('news.html', {
                              'system_message': None,
                              'milestone_complete': milestone_complete,
                              }, RequestContext(request))


def initiative_started(request):
    initiatives_list = initiatives_sponsor()
    paginator = Paginator(initiatives_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        initiatives = paginator.page(page)
    except PageNotAnInteger:
        initiatives = paginator.page(1)
    except EmptyPage:
        initiatives = paginator.page(paginator.num_pages)

    return render_to_response('news.html', {
                              'system_message': None,
                              'initiatives': initiatives,
                              }, RequestContext(request))


def services_requested(request):
    init_service_list = news_dao.initiative_service_needed()
    paginator = Paginator(init_service_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        init_service = paginator.page(page)
    except PageNotAnInteger:
        init_service = paginator.page(1)
    except EmptyPage:
        init_service = paginator.page(paginator.num_pages)
    return render_to_response('news.html', {
                              'system_message': None,
                              'init_service': init_service,
                              }, RequestContext(request))


def services_contributed(request):
    init_service_offer_list = news_dao.initiative_service_contibutions()
    paginator = Paginator(init_service_offer_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        init_service_offer = paginator.page(page)
    except PageNotAnInteger:
        init_service_offer = paginator.page(1)
    except EmptyPage:
        init_service_offer = paginator.page(paginator.num_pages)
    return render_to_response('news.html', {
                              'system_message': None,
                              'init_service_offer': init_service_offer,
                              }, RequestContext(request))


def initiatives_sponsor():
    return Initiative.objects.filter(is_public=True).values(
        'short_desc',
        'create_date',
        'uuid',
        'profile__first_name',
        'profile__last_name'
    ).order_by('-create_date')
