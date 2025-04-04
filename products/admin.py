from django.conf import settings
from django.contrib import admin
from .models import Product , Category
from reviews.models import Review



if not settings.DEBUG:
    from cloudinary.forms import CloudinaryFileField

class ProduitAdmin(admin.ModelAdmin):
    if not settings.DEBUG:
        formfield_overrides = {
            'image': {'widget': CloudinaryFileField},
        }

admin.site.register(Product, ProduitAdmin)

admin.site.register(Category)
admin.site.register(Review)

