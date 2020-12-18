from django.shortcuts import render, get_object_or_404
from .models import Review
from product.models import Product
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewPagination, ReviewRateSerializer
# Create your views here.



class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Review.objects.filter(verified=True)
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    
    def get_queryset(self):
        queryset = Review.objects.filter(approved=True)
        product_slug = self.request.query_params.get('product_slug', None)
        if product_slug is not None:
            try:
                queryset = queryset.filter(product__slug=product_slug)
            except:
                pass
        return queryset


class CreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    # lookup_fields = 'product__slug'

    @classmethod
    def get_client_ip(cls, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def perform_create(self, serializer):
        if 'slug' in self.kwargs:
            slug = self.kwargs.get('slug')
            user_source = self.request.META.get("HTTP_REFERER", "")
            user_ip = self.get_client_ip(request=self.request)
            product_instance = get_object_or_404(Product, slug=slug)
        return serializer.save(product=product_instance, ip_address=user_ip, source=user_source)


class RateReview(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewRateSerializer
    lookup_fields = 'pk'

    # def put(self, request, *args, **kwargs):
        
    #     return self.update(request, *args, **kwargs)