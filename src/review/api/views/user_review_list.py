from django.db.models import F, BigIntegerField
from django.db.models.functions import Cast
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import ReviewSerializer
from ...models import Review


class UserReviewListAPIView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('comment',)
    ordering_fields = ('helpfulness', 'date_created', 'score')

    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user,
        ).annotate(
            helpfulness=
                Cast(F('like'),output_field=BigIntegerField()) - 
                Cast(F('dislike'), output_field=BigIntegerField()), 
        )