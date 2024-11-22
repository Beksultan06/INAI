from django.db import models

from apps.base.models import Order
from apps.users.models import User

# Create your models here.
class Vehicle(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название транспортного средства"
    )
    license_plate = models.CharField(
        max_length=50,
        verbose_name="Номерной знак",
        unique=True
    )
    capacity = models.PositiveIntegerField(
        verbose_name="Вместимость (в кг)"
    )
    available = models.BooleanField(
        default=True,
        verbose_name="Доступно"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    def mark_unavailable(self):
        """Обозначить транспортное средство как недоступное"""
        self.available = False
        self.save()

    def mark_available(self):
        """Обозначить транспортное средство как доступное"""
        self.available = True
        self.save()

    def __str__(self):
        return f"{self.name} ({self.license_plate})"

    class Meta:
        verbose_name_plural = 'Транспортное средство'

class Route(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('in_progress', 'В пути'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ"
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        verbose_name="Транспортное средство"
    )
    courier = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Курьер"
    )
    start_location = models.CharField(
        max_length=255,
        verbose_name="Начальная точка"
    )
    end_location = models.CharField(
        max_length=255,
        verbose_name="Конечная точка"
    )
    distance = models.FloatField(
        verbose_name="Дистанция (в км)"
    )
    estimated_time = models.DurationField(
        verbose_name="Ожидаемое время доставки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания маршрута"
    )
    status = models.CharField(
        max_length=50,
        verbose_name='Статус',
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return f"Маршрут для заказа {self.order.id}"

    def start_route(self):
        """Начать выполнение маршрута"""
        self.status = 'in_progress'
        self.save()

    def complete_route(self):
        """Завершить маршрут"""
        self.status = 'completed'
        self.vehicle.mark_available()
        self.save()

    @classmethod
    def completed_routes_count(cls):
        return cls.objects.filter(status='completed').count()

    @classmethod
    def total_distance(cls):
        return cls.objects.aggregate(total=models.Sum('distance'))['total']

    @property
    def cost(self):
        """
        Рассчитывает стоимость доставки на основе расстояния.
        """
        base_rate = 50
        return self.distance * base_rate

    class Meta:
        verbose_name_plural = 'Маршрут'