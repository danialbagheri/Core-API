from django.db.models import F, BigIntegerField
from django.db.models.functions import Cast
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from ..filters import ReviewFilter
from ..paginations import ReviewPagination
from ..serializers import ReviewSerializer
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
        ).annotate(
            helpfulness=
                Cast(F('like'),output_field=BigIntegerField()) - 
                Cast(F('dislike'), output_field=BigIntegerField()), 
        )
