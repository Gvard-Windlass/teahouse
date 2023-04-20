from django.contrib import admin

from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "get_user_first_name",
        "get_user_last_name",
        "get_user_email",
        "birthday",
        "avatar",
        "is_staff",
    )
    search_fields = ("user__username", "user__first_name", "user__last_name" "birthday")
    list_filter = ("user__is_staff",)
    exclude = ("user",)

    @admin.display(description="first name")
    def get_user_first_name(self, obj: Customer):
        return obj.user.first_name

    @admin.display(description="last name")
    def get_user_last_name(self, obj: Customer):
        return obj.user.last_name

    @admin.display(description="email")
    def get_user_email(self, obj: Customer):
        return obj.user.email

    @admin.display(description="staff?")
    def is_staff(self, obj: Customer):
        return obj.user.is_staff
