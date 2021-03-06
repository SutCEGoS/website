__author__ = 'mjafar'

import hashlib
import urllib

from django import template

register = template.Library()


class GravatarUrlNode(template.Node):
    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        size = 40

        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?"
        gravatar_url += urllib.parse.urlencode({'d': 'identicon', 's': str(size)})

        return gravatar_url


@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument", token.split_contents[0])

    return GravatarUrlNode(email)
