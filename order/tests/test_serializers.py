import pytest

# Importa as factories dos locais corretos
from product.factories import ProductFactory
from order.factories import OrderFactory

# Importa o serializer que será testado
from order.serializers import OrderSerializer

# A marcação @pytest.mark.django_db é essencial para permitir acesso ao banco de dados.


@pytest.mark.django_db
def test_order_serializer_calculates_total_correctly():
    """
    Verifica se o OrderSerializer calcula o campo 'total'
    como a soma dos preços dos produtos no pedido.
    """
    # --- 1. Preparação (Arrange) ---
    # Cria dois produtos com preços definidos para termos um resultado esperado.
    product1 = ProductFactory(price=100)  # Ex: R$ 100
    product2 = ProductFactory(price=150)  # Ex: R$ 150
    expected_total = 250

    # Cria um pedido e associa os produtos a ele usando a relação 'products'.
    order = OrderFactory(products=[product1, product2])

    # --- 2. Ação (Act) ---
    # Instancia o serializer com o objeto do pedido.
    serializer = OrderSerializer(instance=order)

    # --- 3. Verificação (Assert) ---
    # Acessa os dados serializados.
    data = serializer.data

    # Verifica se o total calculado pelo serializer é o esperado.
    assert data["total"] == expected_total

    # Verifica se a quantidade de produtos serializados está correta.
    assert len(data["products"]) == 2
