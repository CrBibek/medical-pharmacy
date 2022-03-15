from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product
from carts.models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.auth.decorators import login_required

# Create your views here.

# Private Function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


#Function for adding quantity item in cart
def add_cart(request, product_id):
    current_user = request.user
    #Getting the product id
    product = Product.objects.get(id=product_id)
    #User is authenticated or not
    if current_user.is_authenticated:  
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key] 
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            id = []
            for item in cart_item:
                id.append(item.id)
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            cart_item.save()
        return redirect('cart')
    
    #User is not authenticated
    else:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
   
        try:
            #Get the cart using cart id
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        
        
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            id = []
            for item in cart_item:
                id.append(item.id)
                        
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                #create new cart item
                item.save()
            
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save()
        return redirect('cart')
    
#Function for removing quantity item in cart
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
   
   
#Removing whole cart item from Remove button
def remove_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
   
   
        
# Cart Function
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        grand_Total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            grand_Total = total
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_Total': grand_Total,
    }        
    
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    grand_Total = 0
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            grand_Total = total
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_Total': grand_Total,
    }        
    
    return render(request, 'store/checkout.html', context)

def thankyou(request):
    return render(request, 'store/thankyou.html')