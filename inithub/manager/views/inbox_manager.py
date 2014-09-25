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
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manager.models import Initiative_Service_Offer
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from manager.constants import RECORDS_PER_PAGE
from manager.dao import inbox_dao


@login_required()
def inbox(request):
    # offer messages
    my_pid = request.session['profile_id']
    system_message = None
    if request.POST:
        offer_id = request.POST['offer_id']
        cmd = request.POST['cmd']
        if cmd == 'accept':
            is_accepted = True
        else:
            is_accepted = False

        i = Initiative_Service_Offer.objects.get(pk=offer_id)
        i.is_accepted = is_accepted
        i.save()
        system_message = "Updated"

    #initiative_list = Initiative.objects.all().filter(is_public=True)

    offer_list = inbox_dao.get_offer_list(my_pid)
    paginator = Paginator(offer_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        offers = paginator.page(1)
    except EmptyPage:
        offers = paginator.page(paginator.num_pages)
    #service_selected = Service.objects.filter(initiative_service__initiative_id=initiative_id)
    #iso = Initiative_Service_Offer.objects.filter(initiative__profile_id=my_pid, service__service_id=initiative__).values('short_desc', 'milestones__is_completed')
    return render_to_response('inbox.html', {
                              'offer_list': offers,
                              'system_message': system_message
                              }, RequestContext(request))


def offer_process(request):
    if request.POST:
        offer_id = request.POST['offer_id']
        cmd = request.POST['cmd']

    return render_to_response(
        'inbox.html', {
            'system_message': cmd + ":" + offer_id}, RequestContext(request))
