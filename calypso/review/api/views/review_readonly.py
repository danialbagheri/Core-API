from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from review.api.paginations import ReviewPagination
from review.api.serializers import (
    ReviewSerializer
)
from ...filters import ReviewFilter
from ...models import Review


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

