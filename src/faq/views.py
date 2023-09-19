from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from product.models import Product
from .models import Faq
from .serializers import FaqSerializer


class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faq.objects.filter(public=True)
    serializer_class = FaqSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        product_slug = self.request.GET.get('slug', False)
        if product_slug:
            product_instance = get_object_or_404(Product, slug=product_slug)  # will break
            queryset = queryset.filter(product=product_instance)
        return queryset
