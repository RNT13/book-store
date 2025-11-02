import pytest
from product.models.product import Product, Category


@pytest.mark.django_db
def test_create_product_model():
    product_data = {
        "title": "Notebook Gamer Avançado",
        "description": "Um notebook potente para jogos e trabalho.",
        "price": 7500,
    }

    product = Product.objects.create(**product_data)

    assert product.title == product_data["title"]
    assert product.description == product_data["description"]
    assert product.price == product_data["price"]

    assert product.id is not None

    assert product.active is True


@pytest.mark.django_db
def test_product_category_relationship():
    category1 = Category.objects.create(title="Eletrônicos", slug="eletronicos")
    category2 = Category.objects.create(title="Computadores", slug="computadores")
    product = Product.objects.create(title="Mouse Sem Fio", price=150)

    product.category.add(category1, category2)

    assert product.category.count() == 2
    assert category1 in product.category.all()
    assert category2 in product.category.all()
