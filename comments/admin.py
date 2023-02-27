from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ("user", "id", "product", "timestamp", "parent")
    search_fields = ("user__username", "product__name", "id")
