from django.shortcuts import render, get_object_or_404
from django.core.mail import mail_managers
from .models import Review
from product.models import Product
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
    
    @classmethod
    def notify_the_admin(cls, data):
        subject = f"A new review has been submitted on {data['user_source']}"
        message = f"""
        Please check the latest reviews by visiting https://service.calypsosun.com
        user ip: {data['user_ip']}
        Product: {data['product_name']}
        """
        mail_managers(subject,message)

    def perform_create(self, serializer):
        if 'slug' in self.kwargs:
            slug = self.kwargs.get('slug')
            user_source = self.request.META.get("HTTP_REFERER", "")
            user_ip = self.get_client_ip(request=self.request)
            product_instance = get_object_or_404(Product, slug=slug)
            self.notify_the_admin(data={
                "user_source":user_source,
                "user_ip":user_ip,
                "product_name":product_instance.name,
            })           
            serializer.is_valid(raise_exception=True)
            return serializer.save(product=product_instance, ip_address=user_ip, source=user_source)
        else:
            raise ValidationError()


class RateReview(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewRateSerializer
    lookup_fields = 'pk'

    # def put(self, request, *args, **kwargs):
        
    #     return self.update(request, *args, **kwargs)