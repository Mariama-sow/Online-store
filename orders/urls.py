from django.urls import path
from .views import ChekoutView,OrderHistoryView , order_confirmationview

app_name = 'orders'

urlpatterns = [
    path('checkout/', ChekoutView.as_view(), name='checkout'),
    path('history/', OrderHistoryView.as_view(), name='history') ,
    path('confirmation/<uuid:uid>/', order_confirmationview , name='order_confirmation'), 
]