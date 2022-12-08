from django import template 

register = template.Library()

@register.filter
def int_divide(value, arg):
    return int(value/arg)*arg