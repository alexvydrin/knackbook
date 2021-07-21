"""
Контроллеры (Views)

Section - Разделы
Article - Статьи
"""
import re
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from authapp.models import User
from likeapp.models import LikeArticle, LikeUser
from notificationapp.models import Notification
from tags.models import Tag
from commentapp.models import Comment
from commentapp.forms import CommentForm
from .models import Section, Article


def main(request):
    """Главная страница"""
    context = {
        'title': 'Knack Book',  # Название закладки в браузере
        'list_name': 'Свежие статьи',  # Наименование списка статей
        'links_section_menu': Section.get_links_section_menu(),
        'tags_menu': Tag.get_tags_menu(),
        'articles': Article.get_articles_five(),
    }
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id)
        if user.first().banned:
            now = datetime.utcnow().replace(tzinfo=utc)
            if now > user.first().banned:
                user.update(banned=None)
        context['notification'] = Notification.notification(request)
    return render(request, 'mainapp/article_list.html', context)


def article_detail_view(request, pk, comment_to=None):
    """Просмотр выбранной статьи и работа с комментариями"""

    # Получаем статью
    # одновременно проверяем на пометку удаления и на признак публикации.
    # Такая дополнительная проверка нужна чтобы нельзя было просмотреть
    # удаленную или неопубликованную статью,
    # вручную указав в адресной строке её url
    if request.user.is_staff or request.user == Article.objects.filter(
            id=pk).first().user:
        article = get_object_or_404(Article, pk=pk, is_active=True)
    else:
        article = get_object_or_404(Article, pk=pk, is_active=True,
                                    is_published=True)
    likes = LikeArticle.objects.filter(is_active=True, article=pk)
    likes_user = LikeUser.objects.filter(is_active=True)
    context = {
        'object': article,  # сама статья

        # общее меню разделов
        'links_section_menu': Section.get_links_section_menu(),

        # общее меню тегов
        'tags_menu': Tag.get_tags_menu(),

        # теги статьи
        'tags_for_article': Tag.objects.filter(article=pk, is_active=True),

        # комментарии для статьи - только первый уровень
        'comments': Comment.get_for_article_level_1(article=pk),

        # комментарий для которого развернут ответ
        'comment_for_answers': comment_to,

        'new_comment': False,

        # количество лайков для статьи
        'likes': len(likes),

        'like_active': len(likes.filter(user=request.user.id)),

        'likes_user': len(
            likes_user.filter(is_active=True, user_to=article.user_id)),

        'like_active_user': len(
            likes_user.filter(is_active=True, user_to=article.user_id,
                              user_from=request.user.id)),
    }

    # Ответы на комментарий
    if comment_to is not None:
        context['answers_for_comment'] = Comment.get_for_comment(
            comment_to=comment_to)

    if request.user.is_authenticated:
        context['notification'] = Notification.notification(request)

    if request.method == 'POST':
        # Комментарий добавлен
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article  # Ссылка на текущую статью
            new_comment.user = request.user  # Ссылка на текущего пользователя
            new_comment.save()
            context['new_comment'] = new_comment
            if article.user != request.user:
                Notification.add_notification(content='комментарий',
                                              user_from=request.user,
                                              user_to=article.user,
                                              article=article,
                                              comment=new_comment
                                              )
            for_moderator = re.search(r'@moderator', new_comment.content)
            if for_moderator:
                moderators = User.objects.filter(is_staff=True)
                for moderator in moderators:
                    Notification.add_notification(content='@moderator',
                                                  user_from=request.user,
                                                  user_to=moderator,
                                                  article=article,
                                                  comment=new_comment
                                                  )

        # context['comment_form'] = comment_form
        context['comment_form'] = CommentForm()
    else:
        context['comment_form'] = CommentForm()

    # Количество комментариев к статье
    context['total_comments'] = Comment.objects.filter(
        article=pk, is_active=True).count()

    return render(request, 'mainapp/article_detail.html', context)


class ArticlesForSectionList(DetailView):
    """Просмотр списка статей для выбранного раздела"""
    model = Section
    template_name = 'mainapp/article_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.get_articles_for_section(self.object)
        context['title'] = 'Статьи в разделе'  # Название закладки в браузере
        context['list_name'] = f'Статьи в разделе: {self.object.name} '
        context['links_section_menu'] = Section.get_links_section_menu()
        context['tags_menu'] = Tag.get_tags_menu()
        if self.request.user.is_authenticated:
            context['notification'] = Notification.notification(self.request)
        return context


class ArticlesForTagList(DetailView):
    """Просмотр списка статей для выбранного тега"""
    model = Tag
    template_name = 'mainapp/article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.get_articles_for_tag(self.object)
        context['title'] = 'Статьи по тегу'  # Название закладки в браузере
        context['list_name'] = f'Статьи по тегу: {self.object.name} '
        context['links_section_menu'] = Section.get_links_section_menu()
        context['tags_menu'] = Tag.get_tags_menu()
        if self.request.user.is_authenticated:
            context['notification'] = Notification.notification(self.request)
        return context


class ArticlesForSearch(ListView):
    """
    Просмотр списка статей для введенного в строку поиска текста,
    с учетом расширенного поиска, при котором добавляются отборы
    по дате изменения статьи и рейтингу статьи (при его активации)
    """
    model = Article
    template_name = 'mainapp/article_search.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('q') == '':
            queryset = []
        else:
            queryset = Article.get_articles_for_search(self.request)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset'] = self.get_queryset()
        context['links_section_menu'] = Section.get_links_section_menu()
        context['tags_menu'] = Tag.get_tags_menu()
        context['text_search'] = self.request.GET.get('q')
        context['flag_search'] = self.request.GET.get('flag_search')
        context['search_date'] = self.request.GET.get('search_date')
        context['search_rating'] = self.request.GET.get('search_rating')
        if self.request.user.is_authenticated:
            context['notification'] = Notification.notification(self.request)
        context['value'] = self.request.GET.get('q')
        return context


def page_help(request):
    """Страница помощь"""
    context = {
        'title': 'Помощь',
        'links_section_menu': Section.get_links_section_menu(),
        'tags_menu': Tag.get_tags_menu(),
        'articles': Article.get_articles_five(),
    }
    if request.user.is_authenticated:
        context['notification'] = Notification.notification(request)
    return render(request, 'mainapp/page_help.html', context)
