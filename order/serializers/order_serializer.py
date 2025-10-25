from rest_framework import serializers
from order.models import Order
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total']
