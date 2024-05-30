from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import BorrowingReadSerializer, BorrowingCreateSerializer
from .models import Borrowing
from .permissions import IsAdminOrOwner
from .filters import BorrowingFilter


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowingFilter

    def get_serializer_class(self):
        if self.action == "POST":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"], url_path="return", permission_classes=[permissions.IsAuthenticated])
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        try:
            borrowing.return_borrowing()
            return Response({"status": "borrowing returned"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)