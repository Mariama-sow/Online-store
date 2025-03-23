import uuid
from django.db import models
from django.conf import settings
from products.models import Product
from users.models import User
from django.core.validators import MinValueValidator

class Order(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours de traitement'),
        ('shipped', 'Expédié'),
        ('delivered', 'Livré'),
        ('cancelled', 'Annulé'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
        )
    shipping_address = models.TextField()
    total = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
        )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
        )

