import pytest
from product.models.product import Product, Category


@pytest.mark.django_db
def test_create_product_model():
    """
    Verifica se um objeto Product pode ser criado corretamente no banco de dados.
    """
    # --- 1. Preparação (Arrange) ---
    # Define os dados para o novo produto.
    product_data = {
        "title": "Notebook Gamer Avançado",
        "description": "Um notebook potente para jogos e trabalho.",
        "price": 7500
    }

    # --- 2. Ação (Act) ---
    # Cria a instância do produto no banco de dados.
    product = Product.objects.create(**product_data)

    # --- 3. Verificação (Assert) ---
    # Verifica se os campos foram salvos corretamente.
    assert product.title == product_data["title"]
    assert product.description == product_data["description"]
    assert product.price == product_data["price"]

    # Verifica se o produto recebeu um ID, confirmando que foi salvo no BD.
    assert product.id is not None

    # Verifica o valor padrão do campo 'active'.
    assert product.active is True


@pytest.mark.django_db
def test_product_category_relationship():
    """
    Verifica se a relação ManyToMany entre Product e Category funciona.
    """
    # --- 1. Preparação (Arrange) ---
    category1 = Category.objects.create(
        title="Eletrônicos", slug="eletronicos")
    category2 = Category.objects.create(
        title="Computadores", slug="computadores")
    product = Product.objects.create(title="Mouse Sem Fio", price=150)

    # --- 2. Ação (Act) ---
    # Adiciona as categorias ao produto.
    product.category.add(category1, category2)

    # --- 3. Verificação (Assert) ---
    # Verifica se o produto agora tem 2 categorias associadas.
    assert product.category.count() == 2
    # Verifica se as categorias corretas estão na relação.
    assert category1 in product.category.all()
    assert category2 in product.category.all()
