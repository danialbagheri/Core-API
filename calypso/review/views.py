from django.shortcuts import render
from .models import Review
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .serializers import ReviewSerializer
# Create your views here.


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Review.objects.filter(verified=True)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(verified=True)
        product_slug = self.request.query_params.get('product_slug', None)
        if product_slug is not None:
            try:
                queryset = queryset.filter(product__slug=product_slug)
            except:
                pass
        return queryset
