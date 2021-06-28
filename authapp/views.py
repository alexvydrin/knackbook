from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import UserLoginForm, UserRegisterForm
from mainapp.views import get_links_section_menu, get_tags_menu, \
    get_articles_five


def login(request):
    """Вход пользователя на сайт"""
    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('main:index'))

    content = {
        'title': 'вход',
        'login_form': login_form,
        'links_section_menu': get_links_section_menu(),
        'tags_menu': get_tags_menu(),
        'articles': get_articles_five(),
    }

    return render(request, 'authapp/login.html', content)


def logout(request):
    """Разлогирование пользователя"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    elif not request.user.is_authenticated:
        register_form = UserRegisterForm()
    else:
        return HttpResponseRedirect(reverse('main:index'))

    content = {
        'title': 'регистрация',
        'register_form': register_form,
        'links_section_menu': get_links_section_menu(),
        'tags_menu': get_tags_menu(),
        'articles': get_articles_five(),
    }

    return render(request, 'authapp/register.html', content)
