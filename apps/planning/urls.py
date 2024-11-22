from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.planning.views import RouteViewSet, VehicleViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')

urlpatterns = [
    path('', include(router.urls)),
]
