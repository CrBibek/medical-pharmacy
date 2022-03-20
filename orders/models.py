from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    amount = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, null=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    order_total = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=50)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #Concat First Name and Last Name
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    #Concat Address Line 1 and Address Line 2
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def __str__(self):
        return self.first_name
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_Name