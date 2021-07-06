"""
Контроллеры (Views)

Section - Разделы
Article - Статьи
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Section, Article
from tags.models import Tag
from commentapp.models import Comment
from commentapp.forms import CommentForm


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


def article_detail_view(request, pk):
    """Просмотр выбранной статьи и работа с комментариями"""

    # Получаем статью и одновременно проверяем на пометку удаления и на признак публикации.
    # Такая дополнительная проверка нужна чтобы нельзя было просмотреть удаленную или неопубликованную статью,
    # вручную указав в адресной строке её url
    article = get_object_or_404(Article, pk=pk, is_active=True, is_published=True)

    context = {
        'object': article,  # сама статья
        'links_section_menu': Section.get_links_section_menu(),  # общее меню разделов - можно вынести в общий контекст
        'tags_menu': Tag.get_tags_menu(),  # общее меню тегов - можно вынести в общий контекст
        'tags_for_article': Tag.objects.filter(article=pk, is_active=True),  # теги статьи - создать метод в модели
        'comments': Comment.get_for_article(article=pk),  # комментарии для статьи
        'new_comment': False
    }

    if request.method == 'POST':
        # Комментарий добавлен
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article  # Ссылка на текущую статью
            new_comment.user = request.user  # Ссылка на текущего пользователя
            new_comment.save()
            context['new_comment'] = new_comment
        context['comment_form'] = comment_form
    else:
        context['comment_form'] = CommentForm()

    return render(request, 'mainapp/article_detail.html', context)


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
