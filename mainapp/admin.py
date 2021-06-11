from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.conf import settings
from .models import User, Section, Article

admin.site.register(User, UserAdmin)
# admin.site.register(settings.AUTH_USER_MODEL, UserAdmin)
admin.site.register(Section)
admin.site.register(Article)
