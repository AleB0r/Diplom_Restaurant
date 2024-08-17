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

        # Увеличение количества ингредиента на складе
        ingredient.quantity += quantity
        ingredient.save()

        # Отправка email поставщику
        subject = f'Запрос на покупку {ingredient.name}'
        message = (
            f'Пользователь {request.user.username} хочет купить {quantity} '
            f'{ingredient.get_measurement_unit_display()} {ingredient.name} у вас.\n'
            f'Пожалуйста, свяжитесь с ним для уточнения деталей.'
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [supplier.email],
            fail_silently=False,
        )

        return Response({'status': 'Запрос отправлен поставщику, количество ингредиента обновлено'}, status=status.HTTP_201_CREATED)