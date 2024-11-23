from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'title', 'details', 'quantity', 'is_active']
        read_only_fields = ['id', 'user']

    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError({"title": "Поле 'title' обязательно."})
        if not data.get('details'):
            raise serializers.ValidationError({"details": "Поле 'details' обязательно."})
        if not isinstance(data.get('quantity'), int) or data.get('quantity') <= 0:
            raise serializers.ValidationError({"quantity": "Количество должно быть положительным числом."})
        return data
