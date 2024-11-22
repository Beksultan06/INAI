from rest_framework import viewsets, permissions, serializers
from django.db.models import Count, Q

from apps.users.models import User
from .models import Route, Vehicle
from .serializers import RouteSerializer, VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления транспортными средствами.
    Только авторизованные пользователи могут видеть, создавать, обновлять и удалять транспорт.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]


class RouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления маршрутами.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Автоматический выбор курьера и транспортного средства.
        """
        default_vehicle = self.get_vehicle_by_priority()
        if not default_vehicle:
            raise serializers.ValidationError({"vehicle": "Нет доступных транспортных средств."})

        default_courier = self.get_least_busy_courier()
        if not default_courier:
            raise serializers.ValidationError({"courier": "Нет доступных курьеров."})

        serializer.save(vehicle=default_vehicle, courier=default_courier)

        default_vehicle.available = False
        default_vehicle.save()

    def get_vehicle_by_priority(self):
        """
        Логика выбора транспорта:
        1. Всегда выбираем "Мотоцикл Honda".
        2. Если такого транспорта нет, выбираем любой "мото".
        """
        vehicle = Vehicle.objects.filter(name__icontains="Мотоцикл Honda", available=True).first()
        if not vehicle:
            vehicle = Vehicle.objects.filter(name__icontains="мото", available=True).first()
        return vehicle

    def get_least_busy_courier(self):
        """
        Логика выбора курьера с минимальной загруженностью.
        Курьеры группируются по количеству активных маршрутов (status='in_progress').
        """
        courier = (
            User.objects.filter(groups__name="Курьеры")
            .annotate(active_routes=Count('route', filter=Q(route__status='in_progress')))
            .order_by('active_routes')
            .first()
        )
        return courier
