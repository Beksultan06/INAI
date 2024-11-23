from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.type import TYPE_USER

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(
        max_length=155,
        verbose_name="номер телефона"
    )
    type_user = models.CharField(
        max_length=50,
        verbose_name='Тип пользователя',
        choices=TYPE_USER,
        default='Клиент',
        blank= True, null=True
    )

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = 'Пользователи'

class Kura(models.Model):
    fio = models.CharField(
        max_length=155,
        verbose_name='ФИО'
    )
    phone_number = models.CharField(
        max_length=25,
        verbose_name='Номер Телефона'
    )
    about_me = models.TextField(
        verbose_name='О себе'
    )
    photo1 = models.ImageField(
        upload_to='Kura',
        verbose_name='Загрузите первую сторону паспорта'
    )
    photo2 = models.ImageField(
        upload_to='Kura',
        verbose_name='Загрузите вторую сторону паспорта'
    )

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name_plural = 'Как стать курой'