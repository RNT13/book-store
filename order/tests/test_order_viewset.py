from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.settings import api_settings

from order.factories import OrderFactory, UserFactory
from product.factories import CategoryFactory, ProductFactory
from order.models import Order
from django.contrib.auth import get_user_model
from product.models.category import Category
from product.models.product import Product

User = get_user_model()


class TestOrderViewSet(APITestCase):

    def setUp(self):
        api_settings.DEFAULT_PAGINATION_CLASS = None

        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.category = CategoryFactory(title="Periféricos")
        self.product = ProductFactory(
            title="Mouse Gamer", price=250.00, category=[self.category]
        )

        self.order = OrderFactory(user=self.user, products=[self.product])

        print("🚀 Orders criadas:", Order.objects.count())

    def test_get_all_orders(self):
        url = reverse("order-list", kwargs={"version": "v1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()["results"]
        self.assertEqual(len(response_data), 1)

        order_data = response_data[0]
        self.assertEqual(len(order_data["products"]), 1)
        product_data = order_data["products"][0]

        self.assertEqual(product_data["title"], self.product.title)
        self.assertEqual(float(product_data["price"]), 250.00)
        self.assertEqual(product_data["category"][0]["title"], self.category.title)

    def test_create_order(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)

        new_product = ProductFactory()
        url = reverse("order-list", kwargs={"version": "v1"})
        data = {"products_id": [new_product.id]}

        response = self.client.post(url, data=data, format="json")
        if response.status_code != status.HTTP_201_CREATED:
            print("❌ Erro na criação do pedido:", response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=new_user)
        self.assertEqual(created_order.user, new_user)
        self.assertEqual(created_order.products.count(), 1)
        self.assertIn(new_product, created_order.products.all())
