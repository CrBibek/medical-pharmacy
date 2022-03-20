from django.contrib import admin

from . models import Payment, Order, OrderProduct
# Register your models here.

class AdminOrder(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'phone_number', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    list_per_page = 10

admin.site.register(Payment)
admin.site.register(Order, AdminOrder)

class AdminOrderProduct(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'created_at']
admin.site.register(OrderProduct, AdminOrderProduct)
