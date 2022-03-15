from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_categorywise'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.detail_product, name='detail_product'),
    path('search/', views.search, name='search'),
]