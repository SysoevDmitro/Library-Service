from django.conf import settings
from rest_framework import viewsets, status
import stripe
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from borrowings.models import Borrowing
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_API_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing__user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'create_stripe_session':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"], url_path="create-stripe-session")
    def create_stripe_session(self, request):
        borrowing_id = request.data["borrowing_id"]
        try:
            borrowing = Borrowing.objects.get(id=borrowing_id, user=request.user)
        except Borrowing.DoesNotExist:
            return Response({"error": "Invalid borrowing id or you do not have permission to access this borrowing."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': borrowing.book.title,
                        },
                        'unit_amount': int(borrowing.book.daily_fee * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL,

            )

            payment = Payment.objects.create(
                status='PENDING',
                type='PAYMENT',
                borrowing=borrowing,
                session_url=session.url,
                session_id=session.id,
                money_to_pay=borrowing.book.daily_fee,
            )

            return Response({'sessionId': session.id, 'sessionUrl': session.url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

