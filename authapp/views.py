from django.contrib import auth
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm, \
    UserEditAvatarForm
from authapp.models import User
from mainapp.models import Section, Article
from tags.models import Tag


class PasswordEditView(PasswordChangeView):
    """Редактирование пароля"""
    template_name = 'authapp/edit_password.html'
    success_url = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['links_section_menu'] = Section.get_links_section_menu()
        content['tags_menu'] = Tag.get_tags_menu()
        content['tags_for_article'] = Tag.get_tags_menu()
        return content


def login(request):
    """Вход пользователя на сайт"""
    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))

    content = {
        'title': 'вход',
        'login_form': login_form,
        'links_section_menu': Section.get_links_section_menu(),
        'tags_menu': Tag.get_tags_menu(),
        'articles': Article.get_articles_five(),
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
        'links_section_menu': Section.get_links_section_menu(),
        'tags_menu': Tag.get_tags_menu(),
        'articles': Article.get_articles_five(),
    }

    return render(request, 'authapp/register.html', content)


def edit_user(request):
    """Редактирование пользователя"""
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()

        if request.method == 'POST':
            edit_form = UserEditForm(request.POST, request.FILES,
                                     instance=request.user)
            if edit_form.is_valid():
                edit_form.save()
                return HttpResponseRedirect(reverse('cabinet:cabinet'))

        edit_form = UserEditForm(instance=request.user)

        content = {
            'title': 'редактирование профиля',
            'edit_form': edit_form,
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': Article.get_articles_five(),
            'avatar': user.avatar
        }

        return render(request, 'authapp/edit_user.html', content)

    return HttpResponseRedirect(reverse('auth:login'))


def delete_user(request, pk):
    """Удаление учентой записи"""
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            if user.is_active:
                user.is_active = False
                user.save()
            return HttpResponseRedirect(reverse('main:index'))

        content = {
            'title': 'удаление профиля',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
        }
        return render(request, 'authapp/delete_user.html', content)
    return HttpResponseRedirect(reverse('auth:login'))


def edit_avatar(request):
    """Редактирование аватарки"""
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()

        if request.method == 'POST':
            edit_form = UserEditAvatarForm(request.POST, request.FILES,
                                           instance=request.user)
            if edit_form.is_valid():
                edit_form.save()
                return HttpResponseRedirect(reverse('auth:edit'))

        edit_form = UserEditAvatarForm(instance=request.user)

        content = {
            'title': 'удаление профиля',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': Article.get_articles_five(),
            'edit_form': edit_form,
            'avatar': user.avatar
        }
        return render(request, 'authapp/edit_avatar.html', content)

    return HttpResponseRedirect(reverse('auth:login'))
