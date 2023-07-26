from rest_framework.generics import ListAPIView

from ..serializers import ProductTypeSerializer
from ...models import ProductType


class ProductTypeListAPIView(ListAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()
    pagination_class = None
