"""Проверка работособности. Автотесты"""

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
# from django.contrib.auth.models import User
from authapp.models import User
from mainapp.models import Article, Section
from tags.models import Tag
import time


class TestMainappSmoke(TestCase):
    """Проверка работособности"""

    def setUp(self):
        """Предустановка, подготовка к тестам"""
        call_command('flush', '--noinput')  # очищаем тестовую базу данных
        # загружаем данные для тестов
        call_command('loaddata', 'tests_db.json')

        # Обзор тестовой БД
        # for section in Section.objects.all():
        #   print(section.name)
        # for article in Article.objects.all():
        #   print(article.title)
        # for tag in Tag.objects.all():
        #   print(tag.name)

        self.client = Client()  # объект для отправки запросов

        # Создаем юзера для тестирования
        self.username = 'test1'
        self.password = 'password_for_test'
        self.user = User.objects.create_user(self.username, 'test@gmail.com', self.password)
        self.user.save()

    def tearDown(self):
        """Приборка после тестов"""
        # сброс индексов
        call_command('sqlsequencereset', 'mainapp')

    def test_db_section(self):
        """
        CRUD Section
        создание, чтение, изменение
        (удаление не тестируем так как это фактически изменение поля is_active)
        """
        # Добавляем новый раздел
        _name = "новый раздел"
        _section_new = Section.objects.create(name=_name)
        # Получаем раздел из БД
        _section_new = None
        _section_db = Section.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_section_db.name, _name)
        self.assertEqual(str(_section_db), _name)  # Проверка __str__
        self.assertTrue(_section_db.is_active)
        self.assertIsNotNone(_section_db.created)
        self.assertIsNotNone(_section_db.edited)
        self.assertEqual(_section_db.created, _section_db.edited)

        # Изменяем раздел
        _name = "новый раздел - изменено"
        _section_db.name = _name
        _section_db.is_active = False
        time.sleep(0.0001)  # чтобы изменилось поле edited
        _section_db.save()
        # Получаем ее из БД
        _section_db = None
        _section_db_2 = Section.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_section_db_2.name, _name)
        self.assertFalse(_section_db_2.is_active)
        self.assertIsNotNone(_section_db_2.created)
        self.assertIsNotNone(_section_db_2.edited)
        self.assertNotEqual(_section_db_2.created, _section_db_2.edited)

    def test_urls_if_not_logged_in(self):
        """
        Проверяем возможность открытия всех страниц,
        доступных без авторизации:

        - Главная страница: '/'
        - Статьи в разделе: '/articles_for_section_list/{section.pk}'
        - Статьи с тегом: '/articles_for_tag_list/tag.pk/'
        - Каждая статья: '/articles/{article.pk}/'
        - Страница авторизации: '/auth/login/'
        - Страница регистрации: '/auth/register/'
        """

        # Сначала все пункты основного меню

        # Главная страница
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Статьи в разделе:
        # /articles_for_section_list/{section.pk}
        for section in Section.objects.all():
            response = self.client.get(f'/articles_for_section_list/{section.pk}/')
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице корректного заголовка
            self.assertContains(response, "Статьи в разделе:")
            self.assertContains(response, section.name)

        # Статьи с тегом:
        # /articles_for_tag_list/tag.pk/
        for tag in Tag.objects.all():
            response = self.client.get(f'/articles_for_tag_list/{tag.pk}/')
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице корректного заголовка
            self.assertContains(response, "Статьи для тега:")
            self.assertContains(response, tag.name)

        # Каждая статья:
        # /articles/{article.pk}/
        for article in Article.objects.all():
            response = self.client.get(f'/articles/{article.pk}/')
            # Проверка статуса
            self.assertEqual(response.status_code, 200)
            # Наличие на странице корректного заголовка
            self.assertContains(response, article.title)
            # Наличие на странице требуемых данных
            self.assertContains(response, "теги:")
            self.assertContains(response, "Создано:")
            self.assertContains(response, "Изменено:")

        # Страница авторизации
        # /auth/login/
        response = self.client.get('/auth/login/')
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице требуемых данных
        self.assertContains(response, "Имя пользователя")
        self.assertContains(response, "Пароль")

        # Страница регистрации
        # /auth/register/
        response = self.client.get('/auth/register/')
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице требуемых данных
        self.assertContains(response, "Имя пользователя")
        self.assertContains(response, "Пароль")
        self.assertContains(response, "Подтверждение пароля")
        self.assertContains(response, "Зарегистрироваться")

    def test_urls_if_logged_in(self):
        """
        Проверяем возможность открытия всех страниц,
        доступных только с авторизацией:
        /cabinet/

        Сначала пытаемся открыть эти страницы без авторизации.
        Должна быть автоматическая переадресация на страницу логина

        Проверяем главную страницу до авторизации
        Затем логинимся
        Проверяем главную страницу после авторизации

        И снова пробуем зайти на все эти страницы, но уже залогиненные
        """

        # Проверяем главную страницу ДО того как авторизировались
        response = self.client.get('/')
        self.assertContains(response, "Войти")
        self.assertContains(response, "Регистрация")
        self.assertNotContains(response, "Выйти")
        self.assertNotContains(response, "Личный кабинет")

        # Пробуем зайти в личный кабинет
        # TODO: Должно перенаправлять на логин - сейчас ошибка

        # Затем логинимся
        self.client.login(username=self.username, password=self.password)

        # Проверяем главную страницу ПОСЛЕ того как авторизировались
        response = self.client.get('/')
        self.assertNotContains(response, "Войти")
        self.assertNotContains(response, "Регистрация")
        self.assertContains(response, "Выйти")
        self.assertContains(response, "Личный кабинет")

        # И снова пробуем зайти на все эти страницы, но уже залогиненные

        # Личный кабинет
        # /cabinet/
        response = self.client.get('/cabinet/')
        # Проверка статуса
        self.assertEqual(response.status_code, 200)
        # Наличие на странице требуемых данных
        self.assertContains(response, "Личный кабинет")
        self.assertContains(response, "Имя")
        self.assertContains(response, "Фамилия")
        self.assertContains(response, "О себе")

    def test_db_article(self):
        """
        CRUD Article
        создание, чтение, изменение
        удаление не тестируем так как это фактически изменение поля is_active)
        """

        # Логинимся
        self.client.login(username=self.username, password=self.password)

        # Добавляем новую статью
        _title = "Новая статья"
        _content = "Содержимое статьи"
        _sections = (1, 2,)  # id разделов в БД
        _tags = (1, 2,)  # id тегов в БД
        _article_new = Article.objects.create(
            title=_title,
            content=_content,
            user=self.user)
        _article_new.sections.set(_sections)  # ManyToMany relationship
        _article_new.tags.set(_tags)  # ManyToMany relationship
        # Получаем ее из БД
        _article_new = None
        _article_db = Article.objects.get(title=_title)
        # Проверяем правильность
        self.assertEqual(_article_db.title, _title)
        self.assertEqual(str(_article_db), _title)  # Проверка __str__
        self.assertEqual(str(_article_db.content), _content)
        self.assertEqual(_article_db.user, self.user)
        self.assertTrue(_article_db.is_active)
        self.assertEqual(_article_db.sections.count(), 2)
        self.assertEqual(_article_db.tags.count(), 2)
        self.assertIsNotNone(_article_db.created)
        self.assertIsNotNone(_article_db.edited)
        self.assertEqual(_article_db.created, _article_db.edited)

        # Изменяем статью
        _title = "новая статья - изменено"
        _content = "Содержимое статьи - изменено"
        _article_db.title = _title
        _article_db.content = _content
        _article_db.is_active = False
        time.sleep(0.0001)  # чтобы изменилось поле edited
        _article_db.save()
        # Получаем ее из БД
        _article_db = None
        _article_db_2 = Article.objects.get(title=_title)
        # Проверяем правильность
        self.assertEqual(_article_db_2.title, _title)
        self.assertEqual(str(_article_db_2.content), _content)
        self.assertEqual(_article_db_2.user, self.user)
        self.assertFalse(_article_db_2.is_active)
        self.assertEqual(_article_db_2.sections.count(), 2)
        self.assertEqual(_article_db_2.tags.count(), 2)
        self.assertIsNotNone(_article_db_2.created)
        self.assertIsNotNone(_article_db_2.edited)
        self.assertNotEqual(_article_db_2.created, _article_db_2.edited)

    def test_db_tag(self):
        """
        CRUD Tag
        создание, чтение, изменение
        (удаление не тестируем так как это фактически изменение поля is_active)
        """

        # Добавляем новый тег
        _name = "новый тег"
        # noinspection DuplicatedCode
        _tag_new = Tag.objects.create(name=_name)
        # Получаем тег из БД
        _tag_new = None
        _tag_db = Tag.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_tag_db.name, _name)
        self.assertEqual(str(_tag_db), _name)  # Проверка __str__
        self.assertTrue(_tag_db.is_active)
        self.assertIsNotNone(_tag_db.created)
        self.assertIsNotNone(_tag_db.edited)
        self.assertEqual(_tag_db.created, _tag_db.edited)

        # Изменяем тег
        _name = "новый тег - изменено"
        _tag_db.name = _name
        _tag_db.is_active = False
        time.sleep(0.0001)  # чтобы изменилось поле edited
        _tag_db.save()
        # Получаем ее из БД
        _tag_db = None
        _tag_db_2 = Tag.objects.get(name=_name)
        # Проверяем правильность
        self.assertEqual(_tag_db_2.name, _name)
        self.assertFalse(_tag_db_2.is_active)
        self.assertIsNotNone(_tag_db_2.created)
        self.assertIsNotNone(_tag_db_2.edited)
        self.assertNotEqual(_tag_db_2.created, _tag_db_2.edited)
