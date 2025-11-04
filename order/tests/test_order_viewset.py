from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from order.factories import OrderFactory, UserFactory
from product.factories import CategoryFactory, ProductFactory
from order.models import Order
from product.models import Product

User = get_user_model()


class TestOrderViewSet(APITestCase):

    def setUp(self):
        self.user = UserFactory()

        self.category = CategoryFactory(title="Periféricos")
        self.product = ProductFactory(
            title="Mouse Gamer", price=250.00, category=[self.category]
        )
        self.order = OrderFactory(user=self.user, products=[self.product])

    def test_get_all_orders_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-list", kwargs={"version": "v1"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIn('count', response_data)
        self.assertIn('results', response_data)
        self.assertEqual(response_data['count'], 1)

        results = response_data['results']
        self.assertEqual(len(results), 1)
        order_data = results[0]
        self.assertEqual(len(order_data["products"]), 1)

        product_data = order_data["products"][0]
        self.assertEqual(product_data["title"], self.product.title)
        self.assertEqual(float(product_data["price"]), 250.00)
        self.assertEqual(product_data["category"]
                         [0]["title"], self.category.title)

    def test_create_order_as_authenticated_user(self):
        new_user = UserFactory()
        new_product = ProductFactory()
        self.client.force_authenticate(user=new_user)

        url = reverse("order-list", kwargs={"version": "v1"})

        data = {"products_id": [new_product.id]}

        response = self.client.post(url, data=data, format="json")

        if response.status_code != status.HTTP_201_CREATED:
            print("❌ Erro na criação do pedido:", response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Order.objects.filter(user=new_user).exists())
        created_order = Order.objects.get(user=new_user)

        self.assertEqual(created_order.products.count(), 1)
        self.assertIn(new_product, created_order.products.all())

    def test_unauthenticated_user_cannot_list_orders(self):
        url = reverse("order-list", kwargs={"version": "v1"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_create_order(self):
        product = ProductFactory()
        url = reverse("order-list", kwargs={"version": "v1"})
        data = {"products": [product.id]}

        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
