from django.urls import path
from .views import main, SectionListView, article_detail_view, ArticleListView, \
    ArticlesForTagList, ArticlesForSectionList, ArticlesForSearch, page_help

app_name = "mainapp"

urlpatterns = [
    path('', main, name='index'),

    path('sections/', SectionListView.as_view(), name='sections'),

    path('articles_for_section_list/<int:pk>/',
         ArticlesForSectionList.as_view(), name='articles_for_section_list'),

    path('articles_for_tag_list/<int:pk>/', ArticlesForTagList.as_view(),
         name='articles_for_tag_list'),

    path('articles/', ArticleListView.as_view(), name='articles'),

    path('articles/<int:pk>/', article_detail_view, name='article_detail'),

    path('articles/search', ArticlesForSearch.as_view(), name='articles_search'),

    path('help/', page_help, name='page_help'),
]
