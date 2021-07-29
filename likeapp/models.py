"""Модели данных"""

from django.db import models
from django.conf import settings
from mainapp.models import Article
from commentapp.models import Comment


class LikeArticle(models.Model):
    """Лайк статьи"""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='статья',
        null=False)
    """статья"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        null=False)
    """пользователь кто поставил лайк"""

    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - лайк активен
    False - лайк удален
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания лайка"""


class LikeComment(models.Model):
    """Лайк комментария (в данной версии пока не используется)"""

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        verbose_name='комментарий',
        null=False)
    """комментарий"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        null=False)
    """пользователь кто поставил лайк"""

    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - лайк активен
    False - лайк удален
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания лайка"""


class LikeUser(models.Model):
    """Лайк пользователя"""

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_to',
        on_delete=models.CASCADE,
        verbose_name='пользователь-получатель',
        null=False)
    """пользователь кому поставлен лайк"""

    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_from',
        on_delete=models.CASCADE,
        verbose_name='пользователь-создатель',
        null=False)
    """пользователь кто поставил лайк"""

    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - лайк активен
    False - лайк удален
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания лайка"""
