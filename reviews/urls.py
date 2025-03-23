# review/urls.py
from django.urls import path
from .views import AddReviewView

app_name = 'reviews'

urlpatterns = [
     path('product/<str:product_uid>/add-review/', AddReviewView.as_view(), name='add_review'),
]