from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь (На основании стандартного пользователя)"""
    MALE = 'Мужской'
    FEMALE = 'Мужской'

    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    banned = models.DateTimeField(
        verbose_name='забанен до',
        null=True,
        blank=True)

    avatar = models.ImageField(upload_to='users_avatars', blank=True,
                               verbose_name='аватар')
    about_me = models.TextField(blank=True, verbose_name='о себе')
    gender = models.CharField(max_length=7, blank=True, choices=GENDER_CHOICES,
                              verbose_name='пол')
    birth_date = models.DateField(blank=True, null=True,
                                  verbose_name='дата рождения')
