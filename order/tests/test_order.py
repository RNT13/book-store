import pytest

from order.factories import OrderFactory
from order.serializers import OrderSerializer
from product.factories import ProductFactory


@pytest.mark.django_db
def test_order_serializer_total():
    product1 = ProductFactory(price=10)
    product2 = ProductFactory(price=20)

    order = OrderFactory(products=[product1, product2])

    serializer = OrderSerializer(order)

    assert serializer.data["total"] == 30
    assert len(serializer.data["products"]) == 2
