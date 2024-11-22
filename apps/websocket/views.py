from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.base.models import Order
from apps.base.serializers import OrderSerializer
from apps.users.models import User


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заказами:
    - CRUD для заказов
    - Обновление статуса заказа
    - Получение списка заказов клиента и курьера
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ограничивает доступ к заказам:
        - Клиенты видят только свои заказы
        - Курьеры видят только назначенные им заказы
        - Администраторы видят все заказы
        """
        user = self.request.user
        if user.role == 'client':
            return Order.objects.filter(client=user)
        elif user.role == 'courier':
            return Order.objects.filter(courier=user)
        return Order.objects.all()

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """
        Обновление статуса заказа.
        Только курьер может менять статус заказа.
        """
        order = get_object_or_404(Order, pk=pk)

        if request.user.role != 'courier':
            return Response({"detail": "Только курьеры могут обновлять статус заказа."},
                            status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if not new_status:
            return Response({"detail": "Необходимо указать новый статус."},
                            status=status.HTTP_400_BAD_REQUEST)

        order.update_status(new_status)
        return Response({"detail": f"Статус заказа обновлён: {new_status}"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_orders(self, request):
        """
        Получение списка заказов для текущего пользователя:
        - Клиенты видят свои заказы
        - Курьеры видят назначенные им заказы
        """
        user = self.request.user
        if user.role == 'client':
            orders = Order.objects.filter(client=user)
        elif user.role == 'courier':
            orders = Order.objects.filter(courier=user)
        else:
            return Response({"detail": "Доступ запрещён."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
