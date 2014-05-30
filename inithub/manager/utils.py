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

from django.conf import settings
from django.core.mail import send_mail
from support.models import Message_Queue
from django.db import IntegrityError
import logging

log = logging.getLogger(__name__)

ID_MASK_KEY = 0xABCDEFAB


def send_internal_email_alert(
        subject,
        body,
        from_email=settings.FROM_EMAIL,
        to_email=settings.INTERNAL_EMAIL,
        fail_silently=True):
    if settings.SEND_INTERNAL_EMAIL_ALERTS:
        send_mail(subject, body, from_email, to_email, fail_silently)


def send_email(subject, body, to_email, fail_silently=False):
    if settings.SEND_EXTERNAL_EMAIL_ALERTS:
        send_mail(subject, body, settings.FROM_EMAIL, to_email, fail_silently)


def queue_internal_email_alert(
        subject,
        body,
        event="INTERNAL",
        from_email=settings.FROM_EMAIL,
        to_email=settings.INTERNAL_EMAIL):
    if settings.SEND_INTERNAL_EMAIL_ALERTS:
        try:
            Message_Queue.objects.create(
                event=event,
                deliver_to=''.join(to_email),
                message_subject=subject,
                message_body=body)
        except IntegrityError:
            log.error('IntegrityError inserting into Message_Queue')


def queue_email(subject, body, to_email, event="UNDEFINED"):
    if settings.SEND_EXTERNAL_EMAIL_ALERTS:
        try:
            Message_Queue.objects.create(
                event=event,
                deliver_to=to_email,
                message_subject=subject,
                message_body=body)
        except IntegrityError:
            log.error('IntegrityError inserting into Message_Queue')


def encode_id(object_id):
    return object_id ^ ID_MASK_KEY


def decode_id(masked_id):
    return masked_id ^ ID_MASK_KEY
