import uuid
from django.db import models
from django.db.models import Sum, F , Count
from users.models import User
from products.models import Product
from django.core.validators import MinValueValidator


class Cart(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    owner = models.OneToOneField(
        User,on_delete=models.CASCADE, related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def amount(self):
        # return self.items.aggregate(
        #     total_amount = Sum(F('quantity')*F('product__price'))  
        # )
        result = self.items.aggregate(
               total_amount=Sum(F('quantity') * F('product__price'))
        )
        return result['total_amount'] or 0  #  Retourne 0 si `None`
    
    @property
    def nb_cart_items(self):
        return self.items.count()
    
class CartItem(models.Model):
    product =models.ForeignKey(
        Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items',
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ['product', 'cart']

    @property
    def total_price(self):
        return self.quantity * self.product.price