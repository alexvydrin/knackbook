from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from authapp.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar',)}),
        (None, {'fields': ('about_me',)}),
        (None, {'fields': ('birth_date',)}),
        (None, {'fields': ('gender',)}),
        (None, {'fields': ('banned',)}),
    )


admin.site.register(User, CustomUserAdmin)
