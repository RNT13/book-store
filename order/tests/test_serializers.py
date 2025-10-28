import pytest

from product.factories import ProductFactory
from order.factories import OrderFactory

from order.serializers import OrderSerializer


@pytest.mark.django_db
def test_order_serializer_calculates_total_correctly():
    product1 = ProductFactory(price=100)
    product2 = ProductFactory(price=150)
    expected_total = 250

    order = OrderFactory(products=[product1, product2])

    serializer = OrderSerializer(instance=order)

    data = serializer.data

    assert data["total"] == expected_total

    assert len(data["products"]) == 2
