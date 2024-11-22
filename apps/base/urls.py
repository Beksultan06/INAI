from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ClientOrderViewSet, CourierOrderViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'client/orders', ClientOrderViewSet, basename='client-orders')
router.register(r'courier/orders', CourierOrderViewSet, basename='courier-orders')

urlpatterns = [
    path('api/', include(router.urls)),
]
