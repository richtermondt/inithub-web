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

RECORDS_PER_PAGE = 25

PROFILE_CREATE_EVENT = 'PROFILE_CREATE'
CONFIRM_ACCOUNT_SUBJECT = 'Please confirm account'

INVITATION_EVENT = 'INVITATION'
INTERNAL_INVITATION_REQUEST_SUBJECT = 'Invitation request'
INTERNAL_INVITATION_REQUEST_BODY = 'A new invitation request has been submitted.'

ACCOUNT_CONFIRMED_EVENT = 'ACCOUNT_CONFIRMED'
ACCOUNT_CONFIRMED_SUBJECT = 'Account confirmed'

ACCESS_REQUEST_APPROVED_EVENT = 'ACCESS_APPROVED'
ACCESS_REQUEST_APPROVED_SUBJECT = 'Access request approved'

USER_INVITE_EVENT = 'USER_INVITE'
USER_INVITE_SUBJECT = 'Your invitation to InitHub'

SUPPORT_TICKET_NEW_EVENT = 'NEW_SUPPORT_TICKET'
SUPPORT_TICKET_REPLY = 'SUPPORT_REPLY'
SUPPORT_TICKET_CUSTOMER_REPLY = 'SUPPORT_CUSTOMER_REPLY'

INITIATIVE_LAUNCH = 'INITIATIVE_LAUNCH'
