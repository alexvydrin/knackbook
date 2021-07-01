"""Модели данных"""

from django.db import models
from django.conf import settings
from mainapp.models import Article
from commentapp.models import Comment


class Notification(models.Model):
    """Уведомление"""

    content = models.TextField(verbose_name='содержимое уведомления')
    """содержимое уведомления"""

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='note_user_to',
        on_delete=models.CASCADE,
        verbose_name='пользователь-получатель',
        null=False)
    """пользователь для кого уведомление"""

    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='note_user_from',
        on_delete=models.CASCADE,
        verbose_name='пользователь-создатель',
        null=False)
    """пользователь от кого уведомление"""

    created = models.DateTimeField(verbose_name='создано', auto_now_add=True)
    """дата и время создания уведомления"""

    closed = models.DateTimeField(verbose_name='закрыто', null=True, blank=True)
    """дата и время закрытия уведомления"""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='статья',
        null=True,
        blank=True)
    """статья"""

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        verbose_name='комментарий',
        null=True,
        blank=True)
    """комментарий"""

    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - уведомление активно
    False - уведомление удалено
    """
