from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing__user=user)

    def get_permissions(self):
        if self.action in ["list", "create"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return permission_classes
