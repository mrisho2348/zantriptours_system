from django import template
from datetime import datetime
register = template.Library()

@register.filter(name='strftime')
def strftime(date, format_string):
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime(format_string)

@register.filter
def truncate_description(description, num_words):
    """
    Truncates a string to the specified number of words.
    """
    words = description.split()
    truncated_words = words[:num_words]
    return ' '.join(truncated_words) + '...'

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='truncate_words')
def truncate_words(value, arg=1000):
    """
    Truncates a string after a certain number of words.
    Argument: Number of words to truncate to.
    """
    words = value.split()
    if len(words) > arg:
        return ' '.join(words[:arg]) + '...'
    else:
        return value