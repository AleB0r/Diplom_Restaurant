from django.urls import path, include
from rest_framework.routers import DefaultRouter

from suppliers.views import SupplierViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
]