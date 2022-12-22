from django.contrib import admin

from .models import *

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'amount')
    search_fields = ('product__name', 'user__username')