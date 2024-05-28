from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library.models import Book


class TestBooks(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="user@email.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_book_401(self):
        self.client.logout()
        url = reverse('library:books-list')
        data = {'title': 'New Book', 'author': 'New Author', 'inventory': 15, 'daily_fee': 9.99}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_201(self):
        url = reverse('library:books-list')
        data = {'title': 'New Book', 'author': 'New Author', 'inventory': 15, 'daily_fee': 9.99}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
