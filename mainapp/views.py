"""
Контроллеры (Views)

**Section - Разделы - CBV CRUD:**
- SectionListView
...

**Article - Статьи - CBV CRUD:**
- ArticleListView
- ArticleDetailView
...

"""

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Section, Article


def main(request):
    """Главная страница"""
    return render(request, 'mainapp/index.html')


class SectionListView(ListView):  # pylint: disable=too-many-ancestors
    """Просмотр списка разделов"""
    model = Section
    template_name = 'mainapp/section_list.html'

    def get_queryset(self):
        filtered_list = self.model.objects.filter(is_active=True).order_by(
            'name')
        return filtered_list


class ArticleListView(ListView):  # pylint: disable=too-many-ancestors
    """Просмотр списка статей"""
    model = Article
    template_name = 'mainapp/article_list.html'

    def get_queryset(self):
        filtered_list = self.model.objects.filter(is_active=True).order_by(
            '-edited', 'title')
        return filtered_list


class ArticleDetailView(DetailView):
    """Просмотр выбранной статьи"""
    model = Article
    template_name = 'mainapp/article_detail.html'
