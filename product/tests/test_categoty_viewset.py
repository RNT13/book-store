from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.factories import CategoryFactory
from product.models import Category


class TestCategoryViewSet(APITestCase):

    def setUp(self):
        self.category = CategoryFactory(title="Livros", slug="livros")

    def test_get_all_categories(self):
        url = reverse('category-list', kwargs={'version': 'v1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['title'], self.category.title)

    def test_create_category(self):
        url = reverse('category-list', kwargs={'version': 'v1'})
        data = {
            'title': "Tecnologia",
            'slug': "tecnologia"
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(slug="tecnologia")
        self.assertEqual(created_category.title, "Tecnologia")
