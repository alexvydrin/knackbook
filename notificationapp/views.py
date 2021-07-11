from datetime import datetime

from django.http import HttpResponseRedirect
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

        if request.method == 'POST':
            if request.POST.get('delete'):
                notification = notifications.filter(
                    id=request.POST.get('delete')).first()
                notification.is_active = False
                notification.save()
            elif request.POST.get('view'):
                notification = notifications.filter(
                    id=request.POST.get('view')).first()
                notification.closed = datetime.now()
                notification.save()

            return HttpResponseRedirect(reverse('notification:notification'))

        content = {
            'title': 'уведомления',
            'links_section_menu': Section.get_links_section_menu(),
            'tags_menu': Tag.get_tags_menu(),
            'score_article': len(score_article),
            'score_article_draft': len(score_article_draft),
            'notifications': notifications.filter(user_to=request.user.id,
                                                  is_active=True).order_by(
                '-created', 'closed'),
            'notification': len(notifications.filter(
                is_active=True,
                user_to=request.user,
                closed=None,
            ))
        }

        return render(request, 'notificationapp/notification.html', content)

    return HttpResponseRedirect(reverse('auth:login'))
