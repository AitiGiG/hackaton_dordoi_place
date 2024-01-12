from django.db import models
from product.models import Product

# Create your models here.

class Review(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(
        'user.User', 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    created_at = models.DateField(auto_now_add=True)
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
