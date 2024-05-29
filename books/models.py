from django.core.validators import URLValidator
from django.db import models


class Book(models.Model):
    HARD = 'HARD'
    SOFT = 'SOFT'
    COVER_CHOICES = [
        (HARD, 'Hardcover'),
        (SOFT, 'Softcover'),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES, default=HARD)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Payment(models.Model):
    PENDING = 'PENDING'
    PAID = 'PAID'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
    ]

    PAYMENT = 'PAYMENT'
    FINE = 'FINE'
    TYPE_CHOICES = [
        (PAYMENT, 'Payment'),
        (FINE, 'Fine'),
    ]
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=PENDING)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default=PAYMENT)
    borrowing = models.ForeignKey("borrowings.Borrowing", on_delete=models.CASCADE)
    session_url = models.URLField(validators=[URLValidator()])
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} for borrowing {self.borrowing_id} - {self.status}"
