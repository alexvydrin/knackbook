from django.urls import path

from mainapp.views import SectionListView, ArticleListView, \
    ArticlesForSectionList, ArticleDetailView

app_name = 'mainapp'

urlpatterns = [
    path('sections/', SectionListView.as_view(), name='sections'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles_for_section_list/<int:pk>/',
         ArticlesForSectionList.as_view(), name='articles_for_section_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(),
         name='article_detail'),
]
