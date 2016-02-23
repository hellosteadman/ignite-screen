from django.template import Library
from django.utils.safestring import mark_safe
import re

register = Library()
HASHTAG_EX = re.compile(r'(#[^ ]+)')
LINK_EX = re.compile(r' (https?://([^ ]+))')
USERNAME_EX = re.compile(r'@([\w]+)')

@register.filter
def tweet(value):
    return mark_safe(
        LINK_EX.sub(' <a href="\g<1>" target="_blank">\g<2></a>',
            HASHTAG_EX.sub(
                '<a href="http://twitter.com/\g<1>" target="_blank">\g<1></a>',
                USERNAME_EX.sub(
                    '@<a href="http://twitter.com/\g<1>" target="_blank">\g<1></a>',
                    value
                )
            )
        )
    )
