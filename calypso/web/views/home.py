from django.conf import settings
from django.views.generic import ListView

from product.models import Product


class HomePage(ListView):
    model = Product
    context_object_name = 'product_categories'
    template_name = 'pages/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['brand_name'] = settings.BRAND_NAME
        return context
