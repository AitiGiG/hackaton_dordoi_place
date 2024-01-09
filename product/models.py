from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        'Category', 
        on_delete=models.CASCADE,
        related_name='products',
    )
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='products',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images', blank=True)
    stock = models.PositiveIntegerField(default=0)
    avalible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.available = False
        super().save(*args, **kwargs)

    