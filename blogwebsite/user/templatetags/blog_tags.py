from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def lookup(dictionary, key):
    return dictionary.get(str(key), False)

@register.filter
def json_script(value):
    return mark_safe(json.dumps(value))