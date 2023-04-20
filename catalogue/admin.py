from django.contrib import admin

from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_type", "price", "amount", "image")
    search_fields = ("name", "image")
    list_filter = ("product_type",)
    exclude = (
        "users_wishlist",
        "users_cart",
        "tea_type",
        "tea_year",
        "utensil_type",
        "utensil_material",
    )


@admin.register(Tea)
class TeaAdmin(admin.ModelAdmin):
    list_display = ("name", "tea_type", "price", "amount", "image", "tea_year")
    search_fields = ("name", "image")
    list_filter = ("tea_type", "tea_year")
    exclude = ("users_wishlist", "users_cart", "utensil_type", "utensil_material")


@admin.register(Utensil)
class UtensilAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "utensil_type",
        "price",
        "amount",
        "image",
        "utensil_material",
    )
    search_fields = ("name", "image")
    list_filter = ("utensil_type", "utensil_material")
    exclude = ("users_wishlist", "users_cart", "tea_type", "tea_year")
