from django import template
from django.apps import apps
from django.db import models

register = template.Library()

@register.filter
def get_type(value):
    return type(value).__name__

@register.filter
def replace_spaces(value):
    return value.replace(' ', '_')

@register.filter
def loop_times(total_pages):
    return range(total_pages)

@register.filter
def get_last_item(lst):
    if lst:
        return lst[-1]
    return None

