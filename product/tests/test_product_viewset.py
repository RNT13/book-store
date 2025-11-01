from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from product.factories import CategoryFactory, ProductFactory
from product.models import Product, Category
from order.factories import UserFactory


class TestProductViewSet(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

        self.category = CategoryFactory(title="Computadores")

        self.product = ProductFactory(
            title="Computador Gamer",
            price=5000.00,
            category=[self.category]
        )

    def test_get_all_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('product-list', kwargs={'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIn('results', response_data)
        results = response_data['results']
        self.assertEqual(len(results), 1)

        product_data = results[0]
        self.assertEqual(product_data['title'], self.product.title)
        self.assertEqual(float(product_data['price']), 5000.00)
        self.assertEqual(product_data['category']
                         [0]['title'], self.category.title)

    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        new_category = Category.objects.filter(slug="tecnologia").first()
        if new_category is None:
            new_category = Category.objects.create(
                title="Notebook Ultra Fino", slug="tecnologia")

        url = reverse('product-list', kwargs={'version': 'v1'})
        data = {
            'title': "Notebook Ultra Fino",
            'price': 3500.00,
            'active': True,
            'categories_id': [new_category.id]
        }

        response = self.client.post(url, data=data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("❌ Erro ao criar produto:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Product.objects.filter(
            title="Notebook Ultra Fino").exists())
        created_product = Product.objects.get(title="Notebook Ultra Fino")
        self.assertEqual(created_product.price, 3500.00)
        self.assertEqual(created_product.category.count(), 1)
        self.assertIn(new_category, created_product.category.all())
