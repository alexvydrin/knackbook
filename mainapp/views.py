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


def get_links_section_menu():
    """Меню разделов"""
    links_section_menu = Section.objects.all()
    return links_section_menu


def get_tegs_menu():
    """Список тегов"""
    # Нужно тут прописать модель таблицы тегов, когда будет, вместо Section
    tegs_menu = Section.objects.all()
    return tegs_menu


def get_articles_five():
    """Пять самых свежих статей по дате создания"""
    articles = Article.objects.all().order_by('-created')[:5]
    return articles


def main(request):
    """Главная страница"""
    context = {
        'title': 'главная',
        'links_section_menu': get_links_section_menu(),
        'tegs_menu': get_tegs_menu(),
        'articles': get_articles_five(),
    }
    return render(request, 'mainapp/index.html', context)


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
