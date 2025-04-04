from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import F
import uuid
from django.core.validators import MinValueValidator



class Category(models.Model):
    uid = models.UUIDField(default=uuid.uuid4 , unique=True)
    name = models.CharField(
        max_length=100, verbose_name='Nom de la categorie'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Catégorie parente"
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique = True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity= models.IntegerField()

    if not settings.DEBUG:
        from cloudinary.models import CloudinaryField
        image = CloudinaryField('image', folder='products')
    else:
        image = models.ImageField(upload_to='products/')
    
    def image_url(self):
        if settings.DEBUG:
            return self.image.url if self.image else ''
        return self.image.url if hasattr(self.image, 'url') else ''
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="products"
    )
    created_at = models.DateTimeField(default=timezone.now, db_index = True)
    is_seen = models.BooleanField(default=False)
     # Ajouter pour gestion stock
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.quantity}"
    
    class Meta : 
        indexes = [
            models.Index(fields=['is_seen', 'price']),
        ]