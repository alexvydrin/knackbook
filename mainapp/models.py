"""Модели данных"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Count, Q

from tags.models import Tag


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

    @staticmethod
    def get_links_section_menu():
        """Меню разделов"""
        links_section_menu = Section.objects.all()
        return links_section_menu


class Article(models.Model):
    """Статья"""

    class Meta:
        ordering = ['-edited']

    title = models.CharField(
        max_length=200,
        verbose_name='название',
        unique=False)
    """наименование статьи"""

    content = models.TextField(verbose_name='контент')
    """контент, содержимое статьи"""

    sections = models.ManyToManyField(
        Section,
        verbose_name='разделы')
    """разделы, в которые входит статья"""

    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги')
    """теги для статьи"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор',
        null=True)
    """автор статьи"""

    rating = models.IntegerField(
        verbose_name='рейтинг',
        default=0,
        db_index=True)
    """рейтинг"""

    is_reviewing = models.BooleanField(
        verbose_name='модерация',
        default=False)
    """статья на модерации"""

    is_published = models.BooleanField(
        verbose_name='опубликована',
        default=False)
    """статья опубликована"""

    is_rejected = models.BooleanField(
        verbose_name='отвергнута',
        default=False)
    """статья отвергнута"""

    reject_comment = models.TextField(
        verbose_name='причина отказа',
        null=True,
        blank=True)
    """комментарий - причина отказа в публикации"""

    review_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='review_user',
        on_delete=models.CASCADE,
        verbose_name='модератор',
        null=True,
        blank=True)
    """модератор статьи"""

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

    @staticmethod
    def get_articles_five():
        """Пять самых свежих статей по дате создания"""
        # Получаем еще количество лайков для статьи
        likes_count = Count('likearticle', filter=Q(likearticle__is_active=True))
        articles = Article.objects.filter(
            is_active=True, is_published=True).annotate(
            likes_count=likes_count).order_by('-edited', 'title')[:5]
        # print("sql:", articles.query)
        return articles

    @staticmethod
    def get_articles_for_section(section):
        """Статьи в разделе"""
        # Получаем еще количество лайков для статьи
        likes_count = Count('likearticle', filter=Q(likearticle__is_active=True))
        articles = Article.objects.filter(
            sections=section,
            is_active=True, is_published=True).annotate(
            likes_count=likes_count).order_by('-edited', 'title')
        # print("sql:", articles.query)
        return articles

    @staticmethod
    def get_articles_for_tag(tag):
        """Статьи для тега"""
        # Получаем еще количество лайков для статьи
        likes_count = Count('likearticle', filter=Q(likearticle__is_active=True))
        articles = Article.objects.filter(
            tags=tag,
            is_active=True, is_published=True).annotate(
            likes_count=likes_count).order_by('-edited', 'title')
        # print("sql:", articles.query)
        return articles

    @staticmethod
    def get_articles_for_search(request):
        """
        Получение списка статей для введенного текста
        поиска (поиск по тексту и названию статьи) +
        расширенный поиск с учетом даты изменения статьи
        и рейтинга
        """
        text_search = request.GET.get('q')
        advanced_search_flag = request.GET.get('flag_search')
        search_date = request.GET.get('search_date')
        search_rating = request.GET.get('search_rating')
        # Получаем еще количество лайков для статьи
        likes_count = Count('likearticle', filter=Q(likearticle__is_active=True))
        # Если расширенный поиск активен - учитываем дополнительные параметры, иначе поиск только по тексту
        if advanced_search_flag == "true":
            articles = Article.objects.filter(
                Q(content__icontains=text_search,
                  edited__gte=search_date,
                  is_active=True,
                  is_published=True) |
                Q(title__icontains=text_search,
                  edited__gte=search_date,
                  is_active=True,
                  is_published=True)).annotate(
                likes_count=likes_count).filter(
                likes_count__gte=search_rating
            ).order_by('-edited', 'title')
        else:
            articles = Article.objects.filter(
                Q(content__icontains=text_search,
                  is_active=True,
                  is_published=True) |
                Q(title__icontains=text_search,
                  is_active=True,
                  is_published=True)).annotate(
                likes_count=likes_count).order_by('-edited', 'title')
        return articles
