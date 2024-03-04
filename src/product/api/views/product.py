from django.db.models import Q
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product
from ..serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.filter(is_public=True)
        product_type = self.request.query_params.get('type', None)
        count = self.request.query_params.get('count', None)

        if product_type is not None:
            try:
                queryset = queryset.filter(
                    Q(types__name__icontains=product_type) |
                    Q(types__slug=product_type)
                )
            except:
                pass
        if count:
            queryset = queryset[:int(count)]
        return queryset
