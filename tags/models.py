"""Модели данных"""

from django.db import models


class Tag(models.Model):
    """Тег"""
    name = models.CharField(
        max_length=100,
        verbose_name='название',
        unique=True)
    """наименование тега"""
    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - тег активен
    False - тег удален
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания тега"""
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    """дата и время последнего изменения тега"""

    def __str__(self):
        return str(self.name)

    @staticmethod
    def get_tags_menu():
        """Метод возвращает список тегов"""
        tags_menu = Tag.objects.all()
        return tags_menu
