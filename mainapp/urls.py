from django.urls import path
from .views import main, SectionListView, ArticleDetailView, ArticleListView, \
    ArticlesForTagList, ArticlesForSectionList

app_name = "mainapp"

urlpatterns = [
    path('', main, name='index'),

    path('sections/', SectionListView.as_view(), name='sections'),

    path('articles_for_section_list/<int:pk>/',
         ArticlesForSectionList.as_view(), name='articles_for_section_list'),

    path('articles_for_tag_list/<int:pk>/', ArticlesForTagList.as_view(),
         name='articles_for_tag_list'),

    path('articles/', ArticleListView.as_view(), name='articles'),

    path('articles/<int:pk>/', ArticleDetailView.as_view(),
         name='article_detail'),
]
