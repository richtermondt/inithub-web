'''

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
