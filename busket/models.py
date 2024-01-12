from django.db import models
from product.models import Product
# Create your models here.

class Busket(models.Model):
    owner = models.ForeignKey('user.User', related_name='buskets', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='buskets', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Корзина для {self.owner.email} | Продукт: {self.product.title}'
    