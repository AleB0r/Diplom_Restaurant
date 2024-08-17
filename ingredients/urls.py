from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import IngredientViewSet, SupplierIngredientViewSet, PurchaseViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'supplier-ingredients', SupplierIngredientViewSet)
router.register(r'purchase', PurchaseViewSet, basename='purchase')

urlpatterns = [
    path('', include(router.urls)),
]
