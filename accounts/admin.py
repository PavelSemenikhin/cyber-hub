from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nickname", "discord", "telegram")
    search_fields = ("nickname", "discord", "telegram")
    list_select_related = ("user",)
    list_filter = ("nickname",)