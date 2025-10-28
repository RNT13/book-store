from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from order.factories import UserFactory
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestProductViewSet(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory(
            title="Computador Gamer",
            price=5000,
        )

    def test_get_all_products(self):
        url = reverse('product-list', kwargs={'version': 'v1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(len(response_data), 1)
        product_data = response_data[0]

        self.assertEqual(product_data['title'], self.product.title)
        self.assertEqual(product_data['price'], self.product.price)
        self.assertEqual(product_data['active'], self.product.active)

    def test_create_product(self):
        category = CategoryFactory()
        url = reverse('product-list', kwargs={'version': 'v1'})
        data = {
            'title': "Notebook Ultra Fino",
            'price': 3500,
            'active': True,
            'categories_id': [category.id]
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title="Notebook Ultra Fino")

        self.assertEqual(created_product.price, 3500)

        self.assertEqual(created_product.category.count(), 1)
        self.assertIn(category, created_product.category.all())
