from django.shortcuts import redirect, render
from carts.models import CartItem
from store.models import Product
from . forms import OrderForm
import datetime 
from . models import Order, OrderProduct, Payment

# Create your views here.

def payment(request):
    
    
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.quantity = item.quantity
        orderproduct.product_id = item.product_id
        
        
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    
    return render(request, 'orders/payment.html')

def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    #If cart count <= 0, redirect to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_Total = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
    
    grand_Total = total 
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #Store Billing Information
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.order_total = grand_Total
            #REMOTE_ADDR gives you user ip
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            #Order ID Generation
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt )
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False,  order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items, 
                'grand_Total': total,
            }
            
            return render(request, 'orders/payment.html', context)
    else:
        return redirect('checkout')