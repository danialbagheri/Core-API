from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Faq
from product.models import Product
from .serializers import FaqSerializer
# Create your views here.

class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faq.objects.filter(public=True)
    serializer_class = FaqSerializer
    lookup_field = "product__slug"

    # def get_queryset(self):
    #     queryset = Faq.objects.filter(public=True)
    #     # queryset = super().get_queryset()
    #     product_slug= self.request.GET.get('slug', False) # "once-a-day-2"
    #     if product_slug:
    #         product_instance = get_object_or_404(Product, slug=product_slug) #will break
    #         queryset = queryset.filter(product=product_instance)
    #     return queryset
    

    
