from datetime import datetime

from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import utc

from authapp.models import User
from cabinetapp.forms import NewArticleForm
from likeapp.models import LikeUser
from mainapp.models import Section, Article
from notificationapp.models import Notification
from tags.models import Tag


def update_is_reviewing(id_article):
    """Отправление статьи на модерацию"""
    Article.objects.filter(id=id_article).update(is_reviewing=True,
                                                 is_published=False,
                                                 is_rejected=False)


def save_draft(id_article):
    """Сохранения черновика"""
    Article.objects.filter(id=id_article).update(is_reviewing=False,
                                                 is_published=False)


def update_article_data(data, pk):
    """Обновление статьи в базе"""
    Article.objects.filter(id=pk).update(
        title=data.get('title'),
        content=data.get('content'),
    )

    Article.objects.filter(id=pk).first().sections.clear()
    Article.objects.filter(id=pk).first().tags.clear()
    for section in data.getlist('sections'):
        Article.objects.filter(id=pk).first().sections.add(section)
    for tag in data.getlist('tags'):
        Article.objects.filter(id=pk).first().tags.add(tag)


def main(request):
    """Главная страница личного кабинета"""
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id)
        likes = LikeUser.objects.filter(user_to=request.user.id)
        if user.first().banned:
            now = datetime.utcnow().replace(tzinfo=utc)
            if now > user.first().banned:
                user.update(banned=None)
        score_article = Article.objects
        score_article_draft = Article.objects.filter(is_active=True,
                                                     is_published=False,
                                                     is_reviewing=False,
                                                     user=request.user.id)
        notification = Notification.objects.filter(
            is_active=True,
            user_to=request.user,
            closed=None,
        )
        if request.user.is_staff:
            score_article = score_article.filter(is_reviewing=True,
                                                 is_active=True)
        elif not request.user.is_staff and not request.user.is_superuser:
            score_article = score_article.filter(is_reviewing=True,
                                                 is_active=True,
                                                 user=request.user.id)

        content = {
            'title': 'личный кабинет',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': Article.get_articles_five(),
            'user': request.user,
            'avatar': user.first().avatar,
            'about_me': user.first().about_me,
            'gender': user.first().gender,
            'birth_date': user.first().birth_date,
            'last_name': user.first().last_name,
            'first_name': user.first().first_name,
            'email': user.first().email,
            'score_article': len(score_article),
            'score_article_draft': len(score_article_draft),
            'notification': len(notification),
            'rating': len(likes),
        }

        return render(request, 'cabinetapp/cabinet.html', content)
    return HttpResponseRedirect(reverse('main:index'))


@user_passes_test(lambda u: not u.banned if u.is_authenticated else '')
def new_article(request):
    """Создание новой статьи"""
    if request.user.is_authenticated:
        form = NewArticleForm(request.POST)

        if request.method == 'POST':
            if form.is_valid():
                create_article = form.save(commit=False)
                create_article.user_id = request.user.id
                if form.data.get('save'):
                    create_article.is_reviewing = True
                form.save()

                return HttpResponseRedirect(reverse('cabinet:cabinet'))

        content = {
            'title': 'личный кабинет',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'form': form,
            'notification': Notification.notification(request)
        }
        return render(request, 'cabinetapp/new_article.html', content)
    return HttpResponseRedirect(reverse('auth:login'))


def my_articles(request):
    """Просмотр моих опубликованных статей"""
    if request.user.is_authenticated:
        user = request.user.id
        articles = Article.objects.filter(
            is_active=True,
            is_published=True,
            user=user
        )

        content = {
            'title': 'мои статьи',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': articles,
            'notification': Notification.notification(request)
        }

        return render(request, 'cabinetapp/my_article.html', content)

    return HttpResponseRedirect(reverse('auth:login'))


def delete_article(request, pk):
    """Удаление статьи"""
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)

        if request.user.id == article.user_id or request.user.is_staff:

            if request.method == 'POST':
                if article.is_active:
                    article.is_active = False
                    article.is_published = False
                    article.save()
                    if request.user != article.user:
                        Notification.add_notification(
                            content='статья удалена',
                            user_from=request.user,
                            user_to=article.user,
                            article=article,
                            comment=None
                            )
                    return HttpResponseRedirect(request.session['next_url'])

            next_url = request.META.get('HTTP_REFERER')
            request.session['next_url'] = next_url

            content = {
                'title': 'удаление статьи',
                'links_section_menu': Section.get_links_section_menu(),
                'tags_menu': Tag.get_tags_menu(),
                'article': article,
                'notification': Notification.notification(request)
            }
            return render(request, 'cabinetapp/delete_article.html', content)

        return HttpResponseRedirect(reverse('cabinet:my_articles'))

    return HttpResponseRedirect(reverse('auth:login'))


def my_drafts(request):
    """Просмотр черновиков"""
    if request.user.is_authenticated:
        user = request.user.id
        articles = Article.objects.filter(
            is_active=True,
            is_published=False,
            is_reviewing=False,
            user=user
        )

        content = {
            'title': 'черновики',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': articles,
            'notification': Notification.notification(request)
        }

        return render(request, 'cabinetapp/my_article.html', content)

    return HttpResponseRedirect(reverse('auth:login'))


def edit_draft(request, pk):
    """Редактирование черновика"""
    if request.user.is_authenticated:
        article = Article.objects.filter(id=pk).first()
        article_published = Article.objects.filter(id=pk,
                                                   is_published=True).first()

        if request.user.id == article.user_id:

            if request.method == 'POST':
                form = NewArticleForm(request.POST)

                if form.is_valid():
                    form.save(commit=False)
                    data = form.data
                    if form.data.get('draft'):
                        save_draft(pk)
                    elif form.data.get('save'):
                        update_is_reviewing(pk)
                    update_article_data(data, pk)

                    return HttpResponseRedirect(reverse('cabinet:my_drafts'))

            form = NewArticleForm(instance=article)

            content = {
                'title': 'редактирование',
                'links_section_menu': Section.get_links_section_menu(),
                'tags_menu': Tag.get_tags_menu(),
                'form': form,
                'article': article,
                'article_published': article_published,
                'notification': Notification.notification(request)
            }

            return render(request, 'cabinetapp/new_article.html', content)

        return HttpResponseRedirect(reverse('cabinet:my_drafts'))

    return HttpResponseRedirect(reverse('auth:login'))


def moderation(request):
    """Список статей на модерации"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            articles = Article.objects.filter(is_reviewing=True,
                                              is_active=True)
        else:
            articles = Article.objects.filter(user=request.user.id,
                                              is_reviewing=True,
                                              is_active=True)

        content = {
            'title': 'модерация',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': articles,
            'notification': Notification.notification(request)
        }

        return render(request, 'cabinetapp/my_article.html', content)
    return HttpResponseRedirect(reverse('auth:login'))


def moderation_check(request, pk, result):
    """Результат модерации"""
    if request.user.is_authenticated:
        article = Article.objects.filter(id=pk).first()
        if request.user.is_staff:
            if request.method == 'POST':
                if result == 1:
                    article.is_reviewing = 0
                    article.is_rejected = 0
                    article.is_published = 1
                    article.reject_comment = None
                elif result == 2:
                    article.is_reviewing = 0
                    article.is_rejected = 1
                    article.is_published = 0
                    article.reject_comment = request.POST.get('comment')
                if request.user != article.user:
                    Notification.add_notification(content=article.reject_comment,
                                                  user_from=request.user,
                                                  user_to=article.user,
                                                  article=article,
                                                  comment=None
                                                  )
                article.review_user_id = request.user.id
                article.save()
                return HttpResponseRedirect(reverse('cabinet:moderation'))

            content = {
                'title': 'модерация статьи',
                'links_section_menu': Section.get_links_section_menu(),
                'tags_menu': Tag.get_tags_menu(),
                'article': article,
                'result': result,
                'notification': Notification.notification(request)
            }

            return render(request, 'cabinetapp/moderation_check.html', content)

        return HttpResponseRedirect(reverse('cabinet:moderation'))
    return HttpResponseRedirect(reverse('auth:login'))
