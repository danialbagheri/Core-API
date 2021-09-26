import uuid

from django.core.mail import mail_managers, mail_admins
from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter

from .filters import ReviewFilter
from .models import Review, Product, ReviewRate
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
    serializer_class = ReviewCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['slug'] = self.kwargs.get('slug', None)
        return context


class RateReview(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewRateSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cookie = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cookie'] = self._cookie
        return context

    def patch(self, request, *args, **kwargs):
        self._cookie = request.COOKIES.get('calypsosun_token', None)
        if not self._cookie:
            self._cookie = uuid.uuid4()
            response = super().patch(request, *args, **kwargs)
            response.set_cookie('calypsosun_token', self._cookie)
            return response
        return super().patch(request, *args, **kwargs)
