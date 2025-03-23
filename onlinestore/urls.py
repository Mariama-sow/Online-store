"""
URL configuration for onlinestore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from users.views import CustomLoginView
from users.views import CustomUserCreationView
from users.views import ActivationUserView
from users.views import LogoutView
from users.views import UserProfilView
from users.views import PasswordResetConfirmView
from users.views import PasswordResetRequestView
from django.conf import settings


urlpatterns = [
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('profile/', UserProfilView.as_view(), name='profile'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/create/', CustomUserCreationView.as_view(), name='create'),
    path('accounts/activation/<str:uid>/<str:token>/', ActivationUserView.as_view(), name='confirm_user_activation'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset_confirm/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('product/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('orders.urls')),
    path('review/', include('reviews.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)