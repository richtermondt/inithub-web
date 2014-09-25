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
from django.template import RequestContext
from manager.models import Service, Services
from django.contrib.auth.decorators import login_required


@login_required()
def service_manager(request):
    system_message = None

    if request.POST:
        sl = request.POST.getlist('service_list')
        Services.objects.filter(
            profile_id=request.session['profile_id']).delete()
        for service in sl:
            Services.objects.create(profile_id=request.session[
                'profile_id'], service_id=service)
        system_message = 'Services updated'
        # return render_to_response('service_manager.html', {
        #                          'system_message': 'Update complete',
        #                          }, context_instance=RequestContext(request))

    s = Service.objects.all().order_by('short_desc', )
    service_selected = Services.objects.get_query_set(
    ).filter(profile_id=request.session['profile_id'])
    return render_to_response('service_manager.html',
                              {'service_list': s,
                               'service_selected': service_selected,
                               'system_message': system_message},
                              RequestContext(request))
