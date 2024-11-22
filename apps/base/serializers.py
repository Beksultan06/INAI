from rest_framework import serializers
from .models import ExtendedOrder, Product, Order, OrderProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'descriptions', 'price', 'created_at', 'photo']
        read_only_fields = ['id', 'created_at']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value

class OrderProductSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_details', 'quantity']
        read_only_fields = ['id', 'product_details']

class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'order_products', 'details', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        order_products_data = validated_data.pop('order_products', [])
        order = Order.objects.create(**validated_data)

        for order_product_data in order_products_data:
            OrderProduct.objects.create(order=order, **order_product_data)

        return order

    def update(self, instance, validated_data):
        order_products_data = validated_data.pop('order_products', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.orderproduct_set.all().delete()

        for order_product_data in order_products_data:
            OrderProduct.objects.create(order=instance, **order_product_data)

        return instance

class ExtendedOrderSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    courier = serializers.StringRelatedField()

    class Meta:
        model = ExtendedOrder
        fields = ['id', 'client', 'courier', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'client', 'courier', 'created_at', 'updated_at']