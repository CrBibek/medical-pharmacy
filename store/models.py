from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_Name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    description = models.TextField(max_length=1000)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    #on_delete CASCADE delete all the products when category is deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    
    #Creating URL form home page product to navigate to detail product page
    def get_url(self):
        return reverse('detail_product', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_Name