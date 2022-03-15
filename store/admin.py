from django.contrib import admin
from . models import Product

# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ('product_Name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_Name',)}

admin.site.register(Product, AdminProduct)