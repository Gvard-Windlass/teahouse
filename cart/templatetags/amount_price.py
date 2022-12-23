from django import template
from django.conf import settings

register = template.Library()

@register.filter
def amount_price(price, amount):
    return amount*price/settings.AMOUNT_STEP

@register.filter
def standard_price(price, amount):
    return amount*price