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