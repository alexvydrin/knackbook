"""
Контроллеры (Views)
"""
import re

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView, DeleteView

from authapp.models import User
from mainapp.models import Section
from notificationapp.models import Notification
from tags.models import Tag
from commentapp.models import Comment
from commentapp.forms import CommentForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


class CommentUpdateView(UpdateView):
    """Изменение комментария"""
    model = Comment
    template_name = 'commentapp/comment_edit.html'
    fields = ['content']

    def get_success_url(self):
        if self.object.comment_level_1 is not None:
            return reverse_lazy('mainapp:article_detail_comment_answers',
                                kwargs={'pk': self.object.article.pk,
                                        'comment_to': self.object.comment_level_1.pk})
        else:
            return reverse_lazy('mainapp:article_detail',
                                kwargs={'pk': self.object.article.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение комментария'
        context[
            'links_section_menu'] = Section.get_links_section_menu()  # общее меню разделов - вынести в общ.контекст
        context[
            'tags_menu'] = Tag.get_tags_menu()  # общее меню тегов - можно вынести в общий контекст
        if self.request.user.is_authenticated:
            context['notification'] = Notification.notification(self.request)
        return context

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: not u.banned))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
@user_passes_test(lambda u: not u.banned)
def comment_create_for_comment(request, pk):
    """Добавление нового комментария в ответ на другой комментарий"""

    # Получаем комментарий и одновременно проверяем на пометку удаления.
    # Такая дополнительная проверка нужна чтобы нельзя было ответить на удаленный комментарий,
    # например вручную указав в адресной строке url
    comment_to = get_object_or_404(Comment, pk=pk, is_active=True)

    context = {
        'links_section_menu': Section.get_links_section_menu(),
        # общее меню разделов - можно вынести в общий контекст
        'tags_menu': Tag.get_tags_menu(),
        # общее меню тегов - можно вынести в общий контекст
    }

    if request.method == 'POST':
        # Комментарий добавлен
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.comment_to = comment_to  # Ссылка на комментарий-родитель
            # Ссылка на комментарий первого уровня
            if comment_to.comment_to is None:
                # Значит ответ на комментарий первого уровня
                new_comment.comment_level_1 = comment_to
            else:
                # Значит ответ на комментарий не первого уровня
                new_comment.comment_level_1 = comment_to.comment_level_1
            new_comment.article = comment_to.article  # Ссылка на текущую статью
            new_comment.user = request.user  # Ссылка на текущего пользователя
            new_comment.save()
            if request.user != comment_to.article.user:
                Notification.add_notification(content='комментарий',
                                              user_from=request.user,
                                              user_to=comment_to.article.user,
                                              article=comment_to.article,
                                              comment=comment_to.comment_to
                                              )
                for_moderator = re.search(r'@moderator', new_comment.content)
                if for_moderator:
                    moderators = User.objects.filter(is_staff=True)
                    for moderator in moderators:
                        Notification.add_notification(content='@moderator',
                                                      user_from=request.user,
                                                      user_to=moderator,
                                                      article=new_comment.article,
                                                      comment=new_comment
                                                      )

            # return redirect('mainapp:article_detail', pk=comment_to.article.pk)
            return redirect('mainapp:article_detail_comment_answers',
                            pk=comment_to.article.pk,
                            comment_to=new_comment.comment_level_1.pk)
        context['comment_form'] = comment_form
    else:
        # Форма для добавления комментария - комментарий еще не добавлен
        context['title'] = 'Ответ на комментарий'
        context['comment_form'] = CommentForm()
        context['notification'] = Notification.notification(request)

    return render(request, 'commentapp/comment_create_for_comment.html',
                  context)


class CommentDeleteView(DeleteView):
    """Удаление комментария"""
    model = Comment
    template_name = 'commentapp/comment_delete.html'

    def get_success_url(self):
        if self.object.comment_level_1 is not None:
            return reverse_lazy('mainapp:article_detail_comment_answers',
                                kwargs={'pk': self.object.article.pk,
                                        'comment_to': self.object.comment_level_1.pk})
        else:
            return reverse_lazy('mainapp:article_detail',
                                kwargs={'pk': self.object.article.pk})

    def __init__(self, *args, **kwargs):
        # self.object потом переопределим в def delete
        # (почему то без определения всех атрибутов в __init__ ругаются линтеры)
        self.object = None
        super().__init__(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        if self.object.user == self.request.user:  # Еще одна дополнительная проверка пользователя
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            'links_section_menu'] = Section.get_links_section_menu()  # общее меню разделов - вынести в общ.контекст
        context[
            'tags_menu'] = Tag.get_tags_menu()  # общее меню тегов - можно вынести в общий контекст
        if self.request.user.is_authenticated:
            context['notification'] = Notification.notification(self.request)
        return context

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: not u.banned))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
