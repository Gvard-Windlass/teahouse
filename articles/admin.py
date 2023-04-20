from django.contrib import admin

from .models import *


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "thumbnail", "publication_date")
    search_fields = ("author", "title", "summary", "body")
    list_filter = ("author", "publication_date")
