from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from authapp.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'banned', 'birth_date', 'avatar', 'gender', 'about_me',)}),
    )


admin.site.register(User, CustomUserAdmin)
