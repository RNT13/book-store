from rest_framework import serializers
from order.models import Order
from product.models import Product
from product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, write_only=True, source="products"
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "products", "products_id", "total"]
        read_only_fields = ["user", "total"]

    def get_total(self, instance):
        return sum([product.price for product in instance.products.all()])
