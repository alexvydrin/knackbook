from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.models import User
from mainapp.models import Section, Article
from tags.models import Tag


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
