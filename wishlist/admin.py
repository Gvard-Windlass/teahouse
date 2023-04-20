from django.contrib import admin

from .models import *


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("product", "user")
    search_fields = ("product__name", "user__username")
