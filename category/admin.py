from django.contrib import admin
from . models import Category

# Register your models here.

class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_Name',)}
    list_display = ('category_Name', 'slug')

admin.site.register(Category, AdminCategory)