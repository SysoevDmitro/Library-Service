from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book
from .models import Borrowing as Borrow


class TestBooks(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="user@email.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_borrowing(self):
        book = Book.objects.create(
            title="Sample",
            author="Name",
            cover="Hard",
            inventory=23,
            daily_fee=2.45,
        )
        data = {
            "book": book.id,
            "borrow_date": "2020-05-21",
            "expected_return_date": "2020-05-30",
        }
        response = self.client.post(reverse("borrowings:borrowings-list"), data)
        print("Borrowing response status code:", response.status_code)  # Print borrowing response status code
        print("Borrowing response content:", response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_borrowing(self):
        book = Book.objects.create(
            title="Sample",
            author="Name",
            cover="Hard",
            inventory=23,
            daily_fee=2.45,
        )
        borrowing = Borrow.objects.create(
            book=book,
            user=self.user,
            borrow_date="2020-05-21",
            expected_return_date="2020-05-30",
        )
        data = {"actual_return_date": "2020-05-31"}
        response = self.client.post(reverse("borrowings:borrowings-return-borrowing", kwargs={"pk": borrowing.id}), data)
        print("Borrowing response status code:", response.status_code)  # Print borrowing response status code
        print("Borrowing response content:", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
