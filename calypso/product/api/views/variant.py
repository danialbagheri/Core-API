from rest_framework import viewsets

from product.models import ProductVariant
from ..serializers import ProductVariantSerializer


class VariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = 'sku'
