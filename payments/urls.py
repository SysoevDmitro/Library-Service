from django.urls import path, include
from .views import PaymentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "payments"
