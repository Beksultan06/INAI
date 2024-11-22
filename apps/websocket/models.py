from django.db import models
from apps.users.models import User

class ChatMessage(models.Model):
    """Модель для сообщений чата."""
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name="Отправитель"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name="Получатель"
    )
    order_id = models.CharField(
        max_length=50,
        verbose_name="ID заказа"
    )
    message = models.TextField(
        verbose_name="Сообщение"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время отправки"
    )

    def __str__(self):
        return f"Сообщение от {self.sender} к {self.receiver}"

    class Meta:
        verbose_name_plural = 'Cообщений чата'