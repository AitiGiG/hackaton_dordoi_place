from django.db import models
from product.models import Product

# Create your models here.

class Favorite(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'user.User',
        related_name='favorite_owners',
        on_delete=models.CASCADE
    )

class Product(models.Model):
    category = models.ForeignKey(
        Product,  
        related_name='products',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'user.User',
        related_name='product_owners',
        on_delete=models.CASCADE
    )

