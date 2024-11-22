from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.throttling import UserRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.base.models import ExtendedOrder, Product, Order
from apps.base.serializers import ExtendedOrderSerializer, ProductSerializer, OrderSerializer
from apps.users.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'descriptions']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('products').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'created_at']
    ordering_fields = ['created_at', 'updated_at']
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClientOrderViewSet(
                         GenericViewSet,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin):
    """
    ViewSet для личного кабинета клиента.
    Показывает только заказы, принадлежащие текущему клиенту.
    """
    serializer_class = ExtendedOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Фильтрует заказы по текущему клиенту.
        """
        return ExtendedOrder.objects.filter(client=self.request.user)

class CourierOrderViewSet(
                          GenericViewSet,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.CreateModelMixin):
    """
    ViewSet для интерфейса курьера.
    Показывает заказы, назначенные текущему курьеру.
    """
    serializer_class = ExtendedOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Фильтрует заказы по текущему курьеру.
        """
        return ExtendedOrder.objects.filter(courier=self.request.user)