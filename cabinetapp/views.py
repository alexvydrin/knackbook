from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from mainapp.views import get_links_section_menu, get_tags_menu, \
    get_articles_five


def main(request):
    context = {
        'title': 'личный кабинет',
        'links_section_menu': get_links_section_menu(),
        'tags_menu': get_tags_menu(),
        'articles': get_articles_five(),
        'user': request.user
    }
    if request.user.is_authenticated:
        return render(request, 'cabinetapp/cabinet.html', context)
    return HttpResponseRedirect(reverse('main:index'))
