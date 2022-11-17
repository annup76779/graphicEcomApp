from django import template
register = template.Library()

@register.filter
def discount(value, arg):
    """
        Returns the calculated discount for the given value
    """
    try:
        value = float(value)
        arg = float(arg)
        return round((value - (value * (arg/100))),2)

    except:pass
    return ""
