from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from mainapp.models import Article, Section
from notificationapp.models import Notification
from tags.models import Tag


def notifications(request):
    """Уведомления"""
    if request.user.is_authenticated:
        notifications = Notification.objects
        score_article_draft = Article.objects.filter(is_active=True,
                                                     is_published=False,
                                                     is_reviewing=False,
                                                     user=request.user.id)
        score_article = Article.objects

        if request.user.is_staff:
            score_article = score_article.filter(is_reviewing=True,
                                                 is_active=True)
        elif not request.user.is_staff and not request.user.is_superuser:
            score_article = score_article.filter(is_reviewing=True,
                                                 is_active=True,
                                                 user=request.user.id)

        content = {
            'title': 'уведомления',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'score_article': len(score_article),
            'score_article_draft': len(score_article_draft),
            'notifications': notifications.filter(user_to=request.user.id,
                                                  is_active=True).order_by(
                '-created'),
            'notification': len(notifications.filter(
                is_active=True,
                user_to=request.user,
                closed=None,
            ))
        }

        return render(request, 'notificationapp/notification.html', content)

    return HttpResponseRedirect(reverse('auth:login'))


@login_required
def notification_edit(request, pk):
    """Изменение статуса уведомления"""
    if request.is_ajax():
        notification = Notification.objects.filter(id=pk,
                                                   closed=None).first()
        if notification:
            notification.closed = datetime.now()
            notification.save()

        return JsonResponse({'result': ''})


@login_required
def notification_delete(request, pk):
    """Удаление уведомления"""
    notifications = Notification.objects

    notification = notifications.filter(id=pk).first()
    if notification:
        notification.is_active = False
        notification.save()

    return JsonResponse({'result': ''})
