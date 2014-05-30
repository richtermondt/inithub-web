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
