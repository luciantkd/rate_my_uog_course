from django import template

register = template.Library()


@register.filter(name='rating_color')
def rating_color(value):
    """Returns a color class based on the value of the rating."""
    try:
        value = int(value)  # Convert value to integer, if it's a string
    except ValueError:
        return ''  # If value is not an integer, return an empty string

    if value < 2:
        return 'low'
    elif value == 2:
        return 'low-medium'
    elif value == 3:
        return 'medium'
    elif value == 4:
        return 'high-medium'
    else:
        return 'high'
