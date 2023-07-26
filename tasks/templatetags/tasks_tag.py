from django import template

# Registering Template
register = template.Library()

# Naming filter to 'range' and adding its functionalities
@register.filter(name='range')
def rangeAlternativeFunctionForTemplates(start, end=None):
    if isinstance(start, int):
        return range(start, end)
    elif isinstance(start, list) or isinstance(start, tuple) or isinstance(start, set) \
        or isinstance(start, dict):
        return range(len(start))
    else:
        return range(end)
    
# Naming filter to 'iseven' and adding its functionalities
@register.filter(name='iseven')
def iseven(value):
    if value % 2 == 0:
        return True
    else:
        return False


# Naming filter to 'iseven' and adding its functionalities
@register.filter(name='length')
def length_of_iterable(value):
    return len(value)