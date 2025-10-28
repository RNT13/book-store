from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.factories import OrderFactory, UserFactory
from product.factories import CategoryFactory, ProductFactory
from order.models import Order


class TestOrderViewSet(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory(title="Periféricos")
        self.product = ProductFactory(
            title="Mouse Gamer",
            price=250,
            categories=[self.category]
        )
        self.order = OrderFactory(user=self.user, products=[self.product])

    def test_get_all_orders(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order-list', kwargs={'version': 'v1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(len(response_data), 1)
        order_data = response_data[0]

        self.assertEqual(len(order_data['products']), 1)
        product_data = order_data['products'][0]

        self.assertEqual(product_data['title'], self.product.title)
        self.assertEqual(product_data['price'], self.product.price)
        self.assertEqual(product_data['category']
                         [0]['title'], self.category.title)

    def test_create_order(self):
        user_for_new_order = UserFactory()
        self.client.force_authenticate(user=user_for_new_order)
        product_to_order = ProductFactory()
        url = reverse('order-list', kwargs={'version': 'v1'})
        data = {
            'products_id': [product_to_order.id]
        }

        response = self.client.post(url, data=data, format='json')

        if response.status_code != status.HTTP_201_CREATED:
            print(f"Erro na criação do pedido: {response.json()}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user_for_new_order)

        self.assertEqual(created_order.user, user_for_new_order)

        self.assertEqual(created_order.products.count(), 1)
        self.assertIn(product_to_order, created_order.products.all())
