import pytest

from order.serializers import OrderSerializer
from order.factories import OrderFactory
from product.factories import ProductFactory


@pytest.mark.django_db
def test_order_serializer_total():
    # Cria produtos fake
    product1 = ProductFactory(price=10)
    product2 = ProductFactory(price=20)

    # Cria pedido fake com produtos
    order = OrderFactory(products=[product1, product2])

    # Serializa
    serializer = OrderSerializer(order)

    # Verifica se o total está correto
    assert serializer.data["total"] == 30
    assert len(serializer.data["products"]) == 2
