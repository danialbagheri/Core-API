from django.core.mail import mail_managers, mail_admins
from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter

from .filters import ReviewFilter
from .models import Review, Product
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewPagination, ReviewRateSerializer


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ReviewFilter
    ordering_fields = ('helpfulness', 'date_created', 'score')
    pagination_class = ReviewPagination

    def get_queryset(self):
        return Review.objects.filter(
            approved=True
        ).annotate(helpfulness=F('like') - F('dislike'))


class CreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

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
        try:
            mail_managers(subject,message)
        except Exception as e:
            mail_admins("New Review Email notification failed", f"{e}")

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
