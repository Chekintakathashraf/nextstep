from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'last_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['ordered_number', 'first_name', 'last_name', 'phone', 'email']

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
