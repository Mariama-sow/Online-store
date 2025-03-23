from django.shortcuts import render
from django.views.generic import ListView , DetailView
from django.db.models import Q
from .models import Product, Category


def home(request):
    return render(request,'products/home.html')

class ProductListView(ListView):
    model = Product
    template_name = 'products/list_product.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)


        # Filtrage par catégorie
        # category_id = self.request.GET.get('category')
        # if category_id:
        #     queryset = queryset.filter(category_id=category_id)
        category_id = self.request.GET.get('category')
        if category_id:
            try:
                category_id = int(category_id)  # ✅ Convertir en entier
                queryset = queryset.filter(category_id=category_id)  # ✅ Fonctionne car `category_id` est un int
            except ValueError:
                queryset = Product.objects.none()  # ✅ Empêche l'erreur si l'ID est invalide

        
        # Recherche
        search = self .request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)|
                Q(description__icontains=search)    
            )

        # Tri
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context
        
           

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail_product.html'
    context_object_name = 'products'
    pk_url_kwarg = 'uid'

    def get_object(self):
        return Product.objects.get(uid=self.kwargs.get('uid'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()[:5]
        return context