from django import template

register = template.Library()

@register.filter
def times(value, arg):
    try:
        return arg * int(value)
    except (ValueError, TypeError):
        return ''
