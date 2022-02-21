from django.views.generic import ListView

from product.models import Product


class HomePage(ListView):
    model = Product
    context_object_name = 'product_categories'
    template_name = 'pages/home.html'
