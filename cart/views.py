from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from products.models import Product
from .models import Cart, CartItem

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_uid = kwargs.get('uid')
        quantity = int(request.POST.get('quantity', 1))

        try:
            product = Product.objects.get(uid=product_uid)
            
            if not request.user.is_authenticated:
                messages.warning(request, "Veuillez vous connecter pour ajouter des produits au panier")
                return redirect('login')
                
            cart, created = Cart.objects.get_or_create(owner=request.user)
             
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                cart=cart,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, "Produit ajouté au panier")
            return redirect('cart:cart_order')
        
        except Product.DoesNotExist:
            messages.error(request, "Produit non trouvé")
            return redirect('products:product_list')


class CartOrderView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'cart/cart_order.html'
    context_object_name = 'cart'
    login_url = 'login'

    def get_object(self):
        cart, created = Cart.objects.get_or_create(owner=self.request.user)
        return cart


class UpdateCartItemView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__owner=request.user)
        
        if quantity > 0 and quantity <= 10:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Quantité mise à jour")
        else:
            messages.warning(request, "Quantité invalide")
            
        return redirect('cart:cart_order')


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__owner=request.user)
        cart_item.delete()
        
        messages.success(request, "Produit retiré du panier")
        return redirect('cart:cart_order')


class ClearCartView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, owner=request.user)
        cart.items.all().delete()
        
        messages.success(request, "Panier vidé avec succès")
        return redirect('cart:cart_order')


class ApplyCouponView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        coupon_code = request.POST.get('coupon_code')
        
        # Ici, vous implémenteriez la logique pour vérifier et appliquer le code promo
        # Exemple simple:
        valid_codes = {
            'BIENVENUE': 10,  # 10% de réduction
            'ETE2023': 5,     # 5% de réduction
        }
        
        if coupon_code in valid_codes:
            cart = get_object_or_404(Cart, owner=request.user)
            discount = valid_codes[coupon_code]
            
            # Stockez la remise dans la session ou dans un champ du modèle Cart
            request.session['discount'] = discount
            request.session['coupon_code'] = coupon_code
            
            messages.success(request, f"Code promo appliqué ! Vous bénéficiez de {discount}% de réduction")
        else:
            messages.error(request, "Code promo invalide ou expiré")
            
        return redirect('cart:cart_order')