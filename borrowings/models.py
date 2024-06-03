from django.db import models
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings")

    def return_borrowing(self):
        if self.actual_return_date:
            raise ValidationError("This borrowing has already been returned")
        self.actual_return_date = timezone.now().date()
        self.book.inventory += 1
        self.book.save()
        self.save()

    @property
    def is_active(self):
        return self.actual_return_date is None

    def save(self, *args, **kwargs):
        if self.pk:
            if self.book.inventory == 0:
                raise ValueError("Cannot borrow a book with zero inventory.")
            self.book.inventory -= 1
            self.book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Borrowing record for {self.book} by {self.user}"
