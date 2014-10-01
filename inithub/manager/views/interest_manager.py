'''

@author: rtermondt
'''
from django.shortcuts import render_to_response
from django.template import RequestContext
from manager.models import Interest, Interests
from django.contrib.auth.decorators import login_required


@login_required()
def interest_manager(request):
    system_message = None
    if request.POST:
        il = request.POST.getlist('interest_list')
        Interests.objects.filter(
            profile_id=request.session['profile_id']).delete()
        for interest in il:
            Interests.objects.create(profile_id=request.session[
                'profile_id'], interest_id=interest)
        system_message = 'Interests updated'
        # return render_to_response('interest_manager.html', {
        #            'system_message': 'Update complete',
        #}, context_instance=RequestContext(request))

    i = Interest.objects.all()
    interest_selected = Interests.objects.get_query_set(
    ).filter(profile_id=request.session['profile_id'])
    return render_to_response('interest_manager.html', {
                              'interest_list': i,
                              'interest_selected': interest_selected,
                              'system_message': system_message
                              }, RequestContext(request))
