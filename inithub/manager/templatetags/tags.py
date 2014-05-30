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
from django import template
from manager import utils
from django.conf import settings

register = template.Library()


@register.tag
def encode_id(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" %
            token.contents.split()[0])
    # if not (isinstance(format_string, long)):
    #    raise template.TemplateSyntaxError("%r tag's argument should be long" % tag_name)
    return EncodeIdNode(format_string)


class EncodeIdNode(template.Node):

    def __init__(self, format_string):
        self.format_string = template.Variable(format_string)

    def render(self, context):

        masked_id = utils.encode_id(long(self.format_string.resolve(context)))
        return masked_id


@register.simple_tag
def secure_url():
    return settings.SECURE_URL


@register.simple_tag
def unsecure_url():
    return settings.UNSECURE_URL


@register.simple_tag
def secure_static_url():
    return settings.SECURE_STATIC_URL


@register.simple_tag
def unsecure_static_url():
    return settings.STATIC_URL
