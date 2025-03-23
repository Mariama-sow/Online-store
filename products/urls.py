from django.urls import path
from .views import ProductListView, ProductDetailView, home

app_name = 'products'

urlpatterns = [
    path('', home, name='home'),
    path('list/', ProductListView.as_view(), name='product_list'),
    path('detail/<uuid:uid>/', ProductDetailView.as_view(), name='product_detail')  
]