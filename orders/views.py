from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Order.objects.all()

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        try:
            order = self.get_object()
            new_status = request.data.get('status')

            if new_status not in dict(Order.STATUS_CHOICES).keys():
                return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

            order.status = new_status
            order.save()
            return Response({'status': 'Order status updated successfully.'}, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

