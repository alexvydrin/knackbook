"""Модели данных"""

from django.db import models
from django.conf import settings
from mainapp.models import Article


class Comment(models.Model):
    """Комментарий"""

    content = models.TextField(verbose_name='содержимое комментария')
    """содержимое комментария"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True)
    """автор комментария"""

    comment_to = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='родитель',
        null=True,
        blank=True)
    """комментарий-родитель"""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='статья',
        null=True,
        blank=True)
    """статья"""

    rating = models.IntegerField(
        verbose_name='рейтинг',
        default=0,
        db_index=True)
    """рейтинг"""

    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - комментарий активен
    False - комментарий удален
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания комментария"""
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    """дата и время последнего изменения комментария"""

    def __str__(self):
        return str(self.content)