"""knackbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('admin/', admin.site.urls, name='admin'),
    path('sections/', mainapp.SectionListView.as_view(), name='sections'),
    path('articles_for_section_list/<int:pk>/', mainapp.ArticlesForSectionList.as_view(),
         name='articles_for_section_list'),
    path('articles_for_tag_list/<int:pk>/', mainapp.ArticlesForTagList.as_view(),
         name='articles_for_tag_list'),
    path('articles/', mainapp.ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', mainapp.ArticleDetailView.as_view(), name='article_detail'),
]
