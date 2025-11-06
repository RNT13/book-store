import pytest

from product.factories import CategoryFactory, ProductFactory
from product.serializers.product_serializer import ProductSerializer


@pytest.mark.django_db
def test_product_serializer_with_categories():
    category1 = CategoryFactory(title="Periféricos")
    category2 = CategoryFactory(title="Promoção")

    product = ProductFactory(title="Teclado Mecânico", price=350, categories=[category1, category2])

    serializer = ProductSerializer(instance=product)
    data = serializer.data

    assert data["title"] == "Teclado Mecânico"
    assert data["price"] == 350
    assert data["active"] is True

    assert len(data["category"]) == 2

    serialized_category_titles = {cat["title"] for cat in data["category"]}

    assert category1.title in serialized_category_titles
    assert category2.title in serialized_category_titles
