from django.template import Library
from django.utils.safestring import mark_safe
import re

register = Library()
HASHTAG_EX = re.compile(r'#([^(?: :#)]+)')

@register.filter
def photo(value):
    return mark_safe(
        HASHTAG_EX.sub(
            '<a href="http://instagram.com/explore/tags/\g<1>" target="_blank">#\g<1></a>',
            value
        )
    )
