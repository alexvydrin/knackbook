from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь (На основании стандартного пользователя)"""
    MALE = 'Мужской'
    FEMALE = 'Женский'

    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    banned = models.DateTimeField(
        verbose_name='забанен до',
        null=True,
        blank=True)
    """забанен до"""

    avatar = models.ImageField(upload_to='users_avatars', blank=True,
                               verbose_name='аватар')
    """аватар"""

    about_me = models.TextField(blank=True, verbose_name='о себе')
    """о себе"""

    gender = models.CharField(max_length=7, blank=True, choices=GENDER_CHOICES,
                              verbose_name='пол')
    """пол"""

    birth_date = models.DateField(blank=True, null=True,
                                  verbose_name='дата рождения')
    """дата рождения"""

    email = models.EmailField(blank=False, null=False, unique=True)
    """электронная почта"""
