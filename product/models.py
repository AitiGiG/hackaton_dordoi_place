from django.db import models
from category.models import Category, Subcategory
class Product(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products',
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.CASCADE,
        related_name='products',
    )
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='products',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images', blank=True)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.available = False
        else:
            self.available = True
        super().save(*args, **kwargs)

    