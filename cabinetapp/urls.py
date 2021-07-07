from django.urls import path

from .views import main, new_article, my_articles, delete_article, my_drafts, \
    edit_draft, moderation, moderation_check

app_name = "cabinetapp"

urlpatterns = [
    path('', main, name='cabinet'),
    path('new-article/', new_article, name='new_article'),
    path('my-articles/', my_articles, name='my_articles'),
    path('my-drafts/', my_drafts, name='my_drafts'),
    path('delete-article/<int:pk>/', delete_article, name='delete_article'),
    path('edit-draft/<int:pk>', edit_draft, name='edit_draft'),
    path('moderation/', moderation, name='moderation'),
    path('moderation_check/<int:pk>/<int:result>', moderation_check, name='moderation_check'),
]
