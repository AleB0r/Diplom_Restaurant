from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('users.urls')),  
    path('api/', include('suppliers.urls')),
    path('api/', include('ingredients.urls')),
    path('api/', include('tables.urls')),
    path('api/', include('client.urls')),
    path('api/', include('reservations.urls')),
    path('api/', include('dishes.urls')),
    path('api/', include('orders.urls')),

]
