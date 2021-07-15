from datetime import datetime, timedelta

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm, \
    UserEditAvatarForm
from authapp.models import User
from mainapp.models import Section, Article
from notificationapp.models import Notification
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
        content['notification'] = Notification.notification(self.request)
        return content


def login_user(request):
    """Вход пользователя на сайт"""
    if not request.user.is_authenticated:
        login_form = UserLoginForm(data=request.POST)
        if request.method == 'POST' and login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect(request.session['next_url'])

        content = {
            'title': 'вход',
            'login_form': login_form,
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'articles': Article.get_articles_five(),
        }

        next_url = request.META.get('HTTP_REFERER')
        request.session['next_url'] = next_url

        return render(request, 'authapp/login.html', content)
    return HttpResponseRedirect(reverse('main:index'))


def logout(request):
    """Разлогирование пользователя"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password2')
            register_form.save()
            login_user = authenticate(username=username, password=password)
            login(request, login_user)
            return HttpResponseRedirect(request.session['next_url'])
    elif not request.user.is_authenticated:
        register_form = UserRegisterForm()
    else:
        return HttpResponseRedirect(reverse('main:index'))

    next_url = request.META.get('HTTP_REFERER')
    request.session['next_url'] = next_url

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
        notification = Notification.objects.filter(
            is_active=True,
            user_to=request.user,
            closed=None,
        )
        user = User.objects.filter(id=request.user.id).first()

        score_article = Article.objects
        score_article_draft = Article.objects.filter(is_active=True,
                                                     is_published=False,
                                                     is_rejected=False,
                                                     is_reviewing=False,
                                                     user=request.user.id)
        if request.user.is_staff:
            score_article = score_article.filter(is_reviewing=True,
                                                 is_active=True)
        elif not request.user.is_staff and not request.user.is_superuser:
            score_article = score_article.filter(is_reviewing=True,
                                                 is_active=True,
                                                 user=request.user.id)

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
            'avatar': user.avatar,
            'score_article': len(score_article),
            'score_article_draft': len(score_article_draft),
            'notification': len(notification)
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
            'notification': Notification.notification(request)
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
            'avatar': user.avatar,
            'notification': Notification.notification(request)
        }
        return render(request, 'authapp/edit_avatar.html', content)

    return HttpResponseRedirect(reverse('auth:login'))


def banned_user(request, pk, article=None):
    """Бан пользователя"""
    if request.user.is_staff:
        user_ban = User.objects.filter(id=pk)
        content = {
            'title': 'блокировка пользователя',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'notification': Notification.notification(request),
            'user_ban': user_ban.first()
        }
        if not user_ban.first().is_staff:
            if request.method == 'POST':
                now = datetime.now()
                if request.POST.get('day'):
                    user_ban.update(banned=now + timedelta(days=1))
                    Notification.add_notification(
                        content='day',
                        user_to=user_ban.first(),
                        user_from=request.user,
                        article=Article.objects.filter(id=article).first(),
                        comment=None
                    )
                elif request.POST.get('week'):
                    user_ban.update(banned=now + timedelta(weeks=2))
                    Notification.add_notification(
                        content='week',
                        user_to=user_ban.first(),
                        user_from=request.user,
                        article=Article.objects.filter(id=article).first(),
                        comment=None
                    )
                return HttpResponseRedirect(reverse('cabinet:moderation'))

            return render(request, 'authapp/ban_user.html', content)

        content['not_ban'] = True
        return render(request, 'authapp/ban_user.html', content)
    return HttpResponseRedirect(reverse('main:index'))
