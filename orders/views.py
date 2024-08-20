from datetime import date

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.permissions import IsAdminOrWaiter
from .models import Order
from .serializers import OrderSerializer, OrderDishSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrWaiter]

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

    @action(detail=False, methods=['get'], url_path='in-progress')
    def in_progress_orders(self, request):
        queryset = self.get_queryset().filter(status__in=['pending'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='completed')
    def completed_orders(self, request):
        queryset = self.get_queryset().filter(status__in=['completed'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='dishes')
    def order_dishes(self, request, pk=None):
        try:
            order = self.get_object()
            dishes = order.order_dishes
            serializer = OrderDishSerializer(dishes, many=True)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

