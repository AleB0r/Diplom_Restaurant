from django.contrib import admin
from django.contrib.admin import AdminSite

from orders.models import Order

# Register your models here.
admin.site.register(Order)