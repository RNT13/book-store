import pytest

# Importa as factories necessárias
from product.factories import ProductFactory, CategoryFactory

# Importa o serializer que será testado
from product.serializers.product_serializer import ProductSerializer


@pytest.mark.django_db
def test_product_serializer_with_categories():
    """
    Verifica se o ProductSerializer serializa um produto
    e suas categorias aninhadas corretamente.
    """
    # --- 1. Preparação (Arrange) ---
    # Cria duas categorias usando a factory.
    category1 = CategoryFactory(title="Periféricos")
    category2 = CategoryFactory(title="Promoção")

    # Cria um produto e associa as duas categorias a ele.
    # Usamos o método 'categories' que definimos na factory.
    product = ProductFactory(
        title="Teclado Mecânico",
        price=350,
        categories=[category1, category2]
    )

    # --- 2. Ação (Act) ---
    # Instancia o serializer com o objeto do produto.
    serializer = ProductSerializer(instance=product)
    data = serializer.data

    # --- 3. Verificação (Assert) ---
    # Verifica os campos principais do produto.
    assert data["title"] == "Teclado Mecânico"
    assert data["price"] == 350
    assert data["active"] is True

    # Verifica os dados aninhados das categorias.
    assert len(data["category"]) == 2

    # Extrai os títulos das categorias serializadas para facilitar a verificação.
    serialized_category_titles = {cat["title"] for cat in data["category"]}

    # Verifica se os títulos das categorias originais estão presentes nos dados serializados.
    assert category1.title in serialized_category_titles
    assert category2.title in serialized_category_titles
