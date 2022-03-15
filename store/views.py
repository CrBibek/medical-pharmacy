from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from category.models import Category
from . models import Product
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.

def store(request, category_slug=None):
    
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_Count = products.count()
    else:
        #Display all the available product in Store
        products = Product.objects.all().filter(is_available = True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_Count = products.count()
        
    context = {
        'products': paged_products,
        'product_Count':product_Count, 
    }
    
    return render(request, 'store/store.html', context)

# Views for detail of product
def detail_product(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product':single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/detail_product.html',context)


# Search Function
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_Name__icontains=keyword))
            product_Count = products.count()
    context = {
        'products': products,
        'product_Count': product_Count
    }
    return render(request, 'store/store.html', context)

