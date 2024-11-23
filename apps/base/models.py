from django.db import models
from apps.base.constant import STATUS_CHOICES
from apps.users.models import User

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    title = models.CharField(
        max_length=155,
        verbose_name='Заголовка'
    )
    quantity = models.IntegerField(
        verbose_name='Количество товара'
    )
    details = models.TextField(
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создание'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    def __str__(self):
        return f"Заказ {self.id} - {self.status}"

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.orderproduct_set.all())

    class Meta:
        verbose_name_plural = 'Заказы'