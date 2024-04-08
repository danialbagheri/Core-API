from rest_framework.viewsets import ReadOnlyModelViewSet

from product.models import ProductType
from ..serializers import ProductTypeSerializer


class ProductTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()
    lookup_field = 'slug'
    pagination_class = None
