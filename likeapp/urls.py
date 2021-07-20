"""
urls for likeapp
"""

from django.urls import path
from likeapp.views import likes_article, likes_user

app_name = "likeapp"

urlpatterns = [
    path('like_article/<int:pk>/', likes_article, name='like'),
    path('like_user/<int:pk>/', likes_user, name='like_user'),
]
