from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product
from ..serializers import SingleProductSerializer


class SingleProductViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Product.objects.filter(is_public=True)
    serializer_class = SingleProductSerializer
    lookup_field = "slug"
