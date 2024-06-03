from rest_framework import serializers
from .models import Borrowing
from books.serializers import BookSerializer


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Borrowing
        fields = ['id', 'borrow_date', 'expected_return_date', 'actual_return_date', 'book', 'user']


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ['expected_return_date', 'book']

    def validate(self, attrs):
        book = attrs.get('book')
        if book.inventory == 0:
            raise serializers.ValidationError("Cannot borrow a book with zero inventory.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date")
