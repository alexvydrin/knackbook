from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.models import User
from cabinetapp.forms import NewArticleForm
from mainapp.models import Section, Article
from tags.models import Tag


def add_user_article(request, id_last_article):
    """Добавления автора статьи"""
    Article.objects.filter(id=id_last_article).update(user=request.user.id)


def update_is_reviewing(request, id_last_article):
    """Отправление статьи на модерацию"""
    Article.objects.filter(id=id_last_article).update(is_reviewing=True)


def update_is_published(request, id_last_article):
    """Опубликовать статью. Удалить после создания модерации"""
    Article.objects.filter(id=id_last_article).update(is_published=True)


def main(request):
    """Главная страница личного кабинета"""
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()

        context = {
            'title': 'личный кабинет',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': Article.get_articles_five(),
            'user': request.user,
            'avatar': user.avatar,
            'about_me': user.about_me,
            'gender': user.gender,
            'birth_date': user.birth_date,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'email': user.email
        }

        return render(request, 'cabinetapp/cabinet.html', context)
    return HttpResponseRedirect(reverse('main:index'))


def new_article(request):
    """Создание новой статьи"""
    if request.user.is_authenticated:
        form = NewArticleForm(request.POST)
        form.fields['tags'].required = False
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                id_last_article = Article.objects.all().order_by('-id')[0].id
                add_user_article(request, id_last_article)
                if form.data.get('save'):
                    update_is_reviewing(request, id_last_article)

                """ !!! удалить после создания модерации !!! """
                update_is_published(request, id_last_article)
                """ !!! удалить после создания модерации !!! """

                return HttpResponseRedirect(reverse('cabinet:cabinet'))

        context = {
            'title': 'личный кабинет',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': Article.get_articles_five(),
            'form': form
        }
        return render(request, 'cabinetapp/new_article.html', context)
    return HttpResponseRedirect(reverse('auth:login'))
