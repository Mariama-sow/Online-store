from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages
from django.db import IntegrityError
from products.models import Product
from .models import Review

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_uid = self.kwargs['product_uid']
        product = get_object_or_404(Product, uid=product_uid)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        try:
            # Crée une nouvelle review
            Review.objects.create(
                product=product,
                user=self.request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Votre avis a été ajouté avec succès.")
        except IntegrityError:
            messages.error(
                request,
                "Vous avez déjà publié une critique pour ce produit. Vous pouvez la modifier mais pas en créer une nouvelle."
            )

        return redirect('products:product_detail', uid=product_uid)