from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь (На основании стандартного пользователя)"""
    banned = models.DateTimeField(
        verbose_name='забанен до',
        null=True,
        blank=True)
