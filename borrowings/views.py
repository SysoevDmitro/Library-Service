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
    queryset = Borrowing.objects.all().select_related("user", "book")
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowingFilter

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    @staticmethod
    def _params_to_bool(qs: str) -> bool:
        return qs.lower() == "true"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def get_queryset(self):
        queryset = self.queryset

        user = self.request.query_params.get("user_id")
        if user:
            user_ids = self._params_to_ints(user)
            queryset = queryset.filter(user_id__in=user_ids)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            is_active_bool = self._params_to_bool(is_active)
            if is_active_bool:
                queryset = queryset.filter(actual_return__isnull=True)
            else:
                queryset = queryset.filter(actual_return__isnull=False)

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        book = serializer.validated_data.get("book")
        book.inventory -= 1
        book.save()
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"], url_path="return", permission_classes=[permissions.IsAuthenticated])
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        try:
            borrowing.return_borrowing()
            return Response({"status": "borrowing returned"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
