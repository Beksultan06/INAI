from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework import mixins, serializers
from rest_framework.viewsets import GenericViewSet

from apps.base.models import  Order
from apps.base.serializers import  OrderSerializer
from apps.users.permissions import IsOwnerOrReadOnly

class OrderViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except serializers.ValidationError as e:
            print(f"Ошибка валидации: {e}")
            raise

def main(request):
    orders = Order.objects.all()
    return render(request, 'base.html', {'orders': orders})

def active_orders(request):
    user = request.user
    active_orders = Order.objects.filter(user=user, status='active')
    return render(request, 'active_orders.html', {'orders': active_orders})