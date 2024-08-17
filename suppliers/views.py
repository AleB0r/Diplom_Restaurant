from rest_framework import viewsets
from .models import Supplier
from .permissions import IsAdminOrPurchaser
from .serializers import SupplierSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrPurchaser]