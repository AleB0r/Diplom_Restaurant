from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Table
from .serializers import TableSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Переключает статус доступности столика."""
        table = self.get_object()
        table.toggle_availability()
        return Response({'status': 'success', 'is_available': table.is_available}, status=status.HTTP_200_OK)
