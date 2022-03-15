from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_Name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=1000)
    
    #Making Category name into plural form in djano admin
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    # Function for URL of Category    
    def get_slug_url(self):
        return reverse('products_by_categorywise', args=[self.slug])
    
    def __str__(self):
        return self.category_Name
    
    