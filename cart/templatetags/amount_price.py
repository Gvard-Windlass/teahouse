from django import template 

register = template.Library()
amount_step = 10

@register.filter
def amount_price(price, amount):
    return amount*price/amount_step