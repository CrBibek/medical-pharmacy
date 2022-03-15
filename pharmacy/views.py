from django.shortcuts import render
from store.models import Product

def index(request):
    
    #Display all the available product in Homepage
    products = Product.objects.all().filter(is_available=True)
    context= {
        'products':products
    }
    return render(request, 'index.html', context)