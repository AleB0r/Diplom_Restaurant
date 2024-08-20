from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.permissions import IsAdminOrManager
from .models import Table
from .serializers import TableSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAdminOrManager]

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        table = self.get_object()
        table.toggle_availability()
        return Response({'status': 'success', 'is_available': table.is_available}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def available(self, request):
        queryset = self.get_queryset().filter(is_available=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
