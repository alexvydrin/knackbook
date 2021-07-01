from django.contrib import admin
from .models import LikeArticle, LikeComment, LikeUser

admin.site.register(LikeArticle)
admin.site.register(LikeComment)
admin.site.register(LikeUser)
