from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Пользователь (На основании стандартного пользователя)"""
    banned = models.DateTimeField(
        verbose_name='забанен до',
        null=True,
        blank=True)


class UserProfile(models.Model):
    """Профиль пользователя"""
    MALE = 'Мужской'
    FEMALE = 'Мужской'

    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True,
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users_avatars', blank=True,
                               verbose_name='аватар')
    about_me = models.TextField(blank=True, verbose_name='о себе')
    gender = models.CharField(max_length=7, blank=True, choices=GENDER_CHOICES,
                              verbose_name='пол')
    age = models.PositiveSmallIntegerField(blank=True, null=True,
                                           verbose_name='возраст')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
