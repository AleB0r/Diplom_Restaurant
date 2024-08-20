from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import settings
from .models import Ingredient, SupplierIngredient
from .serializers import IngredientSerializer, SupplierIngredientSerializer, PurchaseSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = [IsAuthenticated]


class SupplierIngredientViewSet(viewsets.ModelViewSet):
    queryset = SupplierIngredient.objects.all()
    serializer_class = SupplierIngredientSerializer
    # permission_classes = [IsAuthenticated]


class PurchaseViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        supplier = serializer.validated_data['supplier']
        ingredient = serializer.validated_data['ingredient']
        quantity = serializer.validated_data['quantity']

        ingredient.quantity += quantity
        ingredient.save()

        subject = f'Purchase request {ingredient.name}'
        message = (
            f'User {request.user.username} wants to buy {quantity}'
            f'{ingredient.get_measurement_unit_display()} {ingredient.name} you have.\n'
            f'Please contact him for details.'
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [supplier.email],
            fail_silently=False,
        )

        return Response({'status': 'Request sent to supplier, ingredient quantity updated'}, status=status.HTTP_201_CREATED)