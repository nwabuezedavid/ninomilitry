from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg if isinstance(value, (int, float)) and isinstance(arg, (int, float)) else 0
