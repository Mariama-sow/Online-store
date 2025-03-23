from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<str:uid>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartOrderView.as_view(), name='cart_order'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('clear/', views.ClearCartView.as_view(), name='clear_cart'),
    path('apply-coupon/', views.ApplyCouponView.as_view(), name='apply_coupon'),
]