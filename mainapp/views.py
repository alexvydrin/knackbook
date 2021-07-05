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
from tags.models import Tag


def main(request):
    """Главная страница"""
    context = {
        'title': 'главная',
        'links_section_menu': Section.get_links_section_menu(),
        'tags_menu': Tag.get_tags_menu(),
        'articles': Article.get_articles_five(),
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
        queryset = super().get_queryset()
        return queryset.filter(is_active=True, is_published=True)


class ArticleDetailView(DetailView):
    """Просмотр выбранной статьи"""
    model = Article
    template_name = 'mainapp/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links_section_menu'] = Section.get_links_section_menu()
        context['tags_menu'] = Tag.get_tags_menu()
        context['tags_for_article'] = Tag.objects.filter(article=self.object,
                                                         is_active=True)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True, is_published=True)


class ArticlesForSectionList(DetailView):
    """Просмотр списка статей для выбранного раздела"""
    model = Section
    template_name = 'mainapp/articles_for_section_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(sections=self.object,
                                                     is_active=True,
                                                     is_published=True).order_by(
            '-edited', 'title')
        context['links_section_menu'] = Section.get_links_section_menu()
        context['tags_menu'] = Tag.get_tags_menu()
        return context


class ArticlesForTagList(DetailView):
    """Просмотр списка статей для выбранного тега"""
    model = Tag
    template_name = 'mainapp/articles_for_tag_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(tags=self.object,
                                                     is_active=True,
                                                     is_published=True).order_by(
            '-edited', 'title')
        context['links_section_menu'] = Section.get_links_section_menu()
        context['tags_menu'] = Tag.get_tags_menu()
        return context
