'''

@author: rtermondt
'''

from django.http import HttpResponse, HttpResponseRedirect


def about(request):
    return HttpResponse("Hello, world. You're at the innohub index.")


def index(request):
    return HttpResponse("Hello, world. You're at the innohub index.")


def isSessionValid(request):
    ret = False
    if 'profile_id' in request.session:
        ret = True

    return ret
