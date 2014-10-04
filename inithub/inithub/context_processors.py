'''
Created on Jun 6, 2014

@author: rtermondt
'''

from django.conf import settings
 
 
def global_settings(request):
    invitation_system_setting = getattr(settings, 'INVITATION_SYSTEM', None)
    
    if invitation_system_setting == True:
        invite_system = True
    else:
        invite_system = False

    return {
        'INVITATION_SYSTEM': invite_system
    }

