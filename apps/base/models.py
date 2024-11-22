from django.db import models
from apps.base.constant import STATUS_CHOICES
from apps.users.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Product(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Имя'
    )
    descriptions = models.TextField(
        verbose_name='Описание'
    )
    price = models.IntegerField(
        verbose_name='Цена'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создание'
    )
    photo = models.ImageField(
        upload_to='product',
        verbose_name='Фото'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Продукты'

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
    products = models.ManyToManyField(
        Product,
        through='OrderProduct',
        verbose_name='Продукты'
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

    def __str__(self):
        return f"Заказ {self.id} - {self.status}"

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.orderproduct_set.all())

    class Meta:
        verbose_name_plural = 'Заказы'

class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    class Meta:
        verbose_name_plural = 'Заказанные продукты'



class ExtendedOrder(Order):
    """Расширенная модель заказа с указанием клиента и курьера."""
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_orders',
        verbose_name="Клиент",
        limit_choices_to={'role': 'client'}
    )
    courier = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courier_orders',
        verbose_name="Курьер",
        limit_choices_to={'role': 'courier'},
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.courier} несёт товар {self.client}"

    def update_status(self, new_status):
        """Обновление статуса заказа и отправка уведомления через WebSocket."""
        self.status = new_status
        self.save()

        # Уведомление через WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'order_{self.id}',
            {
                'type': 'order_status_update',
                'message': f'Статус заказа обновлён: {self.status}'
            }
        )

    class Meta:
        verbose_name_plural = 'Расширенный заказ'