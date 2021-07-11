"""
Контроллеры (Views)
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView, DeleteView
from mainapp.models import Section
from notificationapp.models import Notification
from tags.models import Tag
from commentapp.models import Comment
from commentapp.forms import CommentForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class CommentUpdateView(UpdateView):
    """Изменение комментария"""
    model = Comment
    template_name = 'commentapp/comment_edit.html'
    fields = ['content']

    def get_success_url(self):
        return reverse_lazy('mainapp:article_detail', kwargs={'pk': self.object.article.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение комментария'
        context['links_section_menu'] = Section.get_links_section_menu()  # общее меню разделов - вынести в общ.контекст
        context['tags_menu'] = Tag.get_tags_menu()  # общее меню тегов - можно вынести в общий контекст
        if self.request.user.is_authenticated:
            context['notification'] = Notification.notification(self.request)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def comment_create_for_comment(request, pk):
    """Добавление нового комментария в ответ на другой комментарий"""

    # Получаем комментарий и одновременно проверяем на пометку удаления.
    # Такая дополнительная проверка нужна чтобы нельзя было ответить на удаленный комментарий,
    # например вручную указав в адресной строке url
    comment_to = get_object_or_404(Comment, pk=pk, is_active=True)

    context = {
        'links_section_menu': Section.get_links_section_menu(),  # общее меню разделов - можно вынести в общий контекст
        'tags_menu': Tag.get_tags_menu(),  # общее меню тегов - можно вынести в общий контекст
    }

    if request.method == 'POST':
        # Комментарий добавлен
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.comment_to = comment_to  # Ссылка на комментарий-родитель
            new_comment.article = comment_to.article  # Ссылка на текущую статью
            new_comment.user = request.user  # Ссылка на текущего пользователя
            new_comment.save()
            Notification.add_notification(content='комментарий',
                                          user_from=request.user,
                                          user_to=comment_to.article.user,
                                          article=comment_to.article,
                                          comment=comment_to.comment_to
                                          )
            return redirect('mainapp:article_detail', pk=comment_to.article.pk)
        context['comment_form'] = comment_form
    else:
        # Форма для добавления комментария - комментарий еще не добавлен
        context['title'] = 'Ответ на комментарий'
        context['comment_form'] = CommentForm()
        context['notification'] = Notification.notification(request)

    return render(request, 'commentapp/comment_create_for_comment.html', context)


class CommentDeleteView(DeleteView):
    """Удаление комментария"""
    model = Comment
    template_name = 'commentapp/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('mainapp:article_detail', kwargs={'pk': self.object.article.pk})

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
        context['links_section_menu'] = Section.get_links_section_menu()  # общее меню разделов - вынести в общ.контекст
        context['tags_menu'] = Tag.get_tags_menu()  # общее меню тегов - можно вынести в общий контекст
        if self.request.user.is_authenticated:
            context['notification'] = Notification.notification(self.request)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
