from rest_framework import serializers
from .models import Vehicle, Route

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'license_plate', 'capacity', 'available', 'created_at']
        read_only_fields = ['id', 'created_at']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'order', 'start_location', 'end_location', 'distance', 'estimated_time', 'vehicle', 'courier']
        read_only_fields = ['vehicle', 'courier']