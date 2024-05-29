from django.urls import path, include
from .views import BorrowingViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'borrowings', BorrowingViewSet, basename='borrowings')

urlpatterns = [
    path('', include(router.urls))
]

app_name = 'borrowings'
