"""Модели данных"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """Пользователь (На основании стандартного пользователя)"""
    banned = models.DateTimeField(
        verbose_name='забанен до',
        null=True)
    """дата и время до которого пользователь заблокирован"""


class Section(models.Model):
    """Раздел (Тематика, Категория)"""
    name = models.CharField(
        max_length=100,
        verbose_name='название',
        unique=True)
    """наименование раздела"""
    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - раздел активен
    False - раздел удален
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания раздела"""
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    """дата и время последнего изменения раздела"""

    def __str__(self):
        return str(self.name)


class Article(models.Model):
    """Статья"""
    title = models.CharField(
        max_length=200,
        verbose_name='название',
        unique=True)
    """наименование статьи"""
    content = models.TextField(verbose_name='контент')
    """контент, содержимое статьи"""
    sections = models.ManyToManyField(
        Section,
        verbose_name='разделы')
    """разделы, в которые входит статья"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True)
    """автор статьи"""
    is_active = models.BooleanField(
        verbose_name='актив',
        default=True,
        db_index=True)
    """
    True - статья активна
    False - статья удалена
    """
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    """дата и время создания статьи"""
    edited = models.DateTimeField(verbose_name='изменен', auto_now=True)
    """дата и время последнего изменения статьи"""

    def __str__(self):
        return str(self.title)
