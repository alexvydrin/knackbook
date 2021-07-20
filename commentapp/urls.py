"""
urls for commentapp
"""

from django.urls import path
from .views import CommentUpdateView, CommentDeleteView, \
    comment_create_for_comment

app_name = "commentapp"

urlpatterns = [
    path('new/<int:pk>/', comment_create_for_comment, name='comment_new'),

    path('edit/<int:pk>/', CommentUpdateView.as_view(), name='comment_edit'),

    path('delete/<int:pk>/', CommentDeleteView.as_view(),
         name='comment_delete'),
]
