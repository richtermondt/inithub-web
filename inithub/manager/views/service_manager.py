'''

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
