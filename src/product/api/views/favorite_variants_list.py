from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import ProductVariantSerializer


class FavoriteVariantListAPIView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        return self.request.user.favorite_variants.filter(is_public=True, product__is_public=True)
