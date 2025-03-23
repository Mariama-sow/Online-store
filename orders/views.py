from django.shortcuts import get_object_or_404, render , redirect
from django.urls import reverse
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart
from .models import Order, OrderItem

class ChekoutView(LoginRequiredMixin,CreateView):
    model = Order
    template_name = 'orders/checkout.html'
    fields = ['shipping_address']

    def form_valid(self,form):
         # Récupérer le panier de l'utilisateur
        try:
            cart = self.request.user.cart
        except Cart.DoesNotExist:
            messages.error(self.request, "Votre panier est vide.")
            return redirect('cart:cart_order')

        if not cart.items.exists():
            messages.error(self.request, "Votre panier est vide.")
            return redirect('cart:cart_order')
        
        # Création de la commande
        order = form.save(commit=False)
        order.user = self.request.user
        order.total = cart.amount 
        order.save()

        # Création des OrderItems
        # Création des OrderItems et mise à jour du stock
        for item in cart.items.all():
            product = item.product
            if product.quantity >= item.quantity:
                product.quantity -= item.quantity  # ✅ Décrémentation du stock
                product.save()  # ✅ Enregistrement dans la base de données
            else:
                messages.error(self.request, f"Stock insuffisant pour {product.name}")
                return redirect('cart:cart_order')  # Empêche la validation si stock insuffisant

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                purchase_price=product.price
            )

        # Vider le panier
        cart.items.all().delete()


        # Message de confirmation
        messages.success(self.request, "Votre commande a été validée avec succès.")

        return redirect(reverse('orders:order_confirmation', kwargs={'uid': order.uid}))

    
class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

def order_confirmationview(request, uid):
    order = get_object_or_404(Order, uid=uid)
    # Vérifiez que l'utilisateur actuel est le propriétaire de la commande
    if request.user != order.user:
        messages.error(request, "Vous n'êtes pas autorisé à voir cette commande.")
        return redirect('orders:history')
    
    return render(request, 'orders/order_confirmation.html', {'order': order})