"""Модели данных"""

from django.db import models
from django.conf import settings
from mainapp.models import Article
from django.db.models import Count, Q


class Comment(models.Model):
    """Комментарий"""

    class Meta:
        ordering = ('created',)

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
        related_name='comment_comment_to',
        on_delete=models.CASCADE,
        verbose_name='родитель',
        null=True,
        blank=True)
    """комментарий-родитель"""

    comment_level_1 = models.ForeignKey(
        'self',
        related_name='comment_comment_level_1',
        on_delete=models.CASCADE,
        verbose_name='родитель первого уровня',
        null=True,
        blank=True)
    """комментарий-родитель первого уровня"""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='статья',
        null=False)
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

    @staticmethod
    def get_for_article(article):
        """Получить комментарии для статьи"""
        # Получаем еще количество ответов к комментарию
        answers_count = Count('comment_comment_level_1', filter=Q(comment_comment_level_1__is_active=True))
        comments = Comment.objects.filter(article=article, is_active=True).annotate(
            answers_count=answers_count)
        # print("sql:", comments.query)
        return comments

    @staticmethod
    def get_for_article_level_1(article):
        """Получить комментарии для статьи"""
        # Получаем еще количество ответов к комментарию
        answers_count = Count('comment_comment_level_1', filter=Q(comment_comment_level_1__is_active=True))
        comments = Comment.objects.filter(article=article, comment_to__isnull=True, is_active=True).annotate(
            answers_count=answers_count)
        # print("sql:", comments.query)
        return comments

    @staticmethod
    def get_for_comment(comment_to):
        """Получить комментарии для комментария"""
        # comments = Comment.objects.filter(comment_to=comment_to, is_active=True)
        comments = Comment.objects.filter(comment_level_1=comment_to, is_active=True)
        return comments
