"""
urls for mainapp
"""

from django.urls import path
from .views import main, article_detail_view, ArticlesForTagList,\
    ArticlesForSectionList, ArticlesForSearch, page_help, feedback

app_name = "mainapp"

urlpatterns = [
    path('', main, name='index'),

    path('articles_for_section_list/<int:pk>/',
         ArticlesForSectionList.as_view(),
         name='articles_for_section_list'),

    path('articles_for_tag_list/<int:pk>/', ArticlesForTagList.as_view(),
         name='articles_for_tag_list'),

    path('articles/<int:pk>/', article_detail_view,
         name='article_detail'),

    path('articles/<int:pk>/<int:comment_to>/', article_detail_view,
         name='article_detail_comment_answers'),

    path('articles/search', ArticlesForSearch.as_view(),
         name='articles_search'),

    path('help/', page_help, name='page_help'),

    path('feedback/', feedback, name='feedback'),
]
