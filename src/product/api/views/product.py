from rest_framework import viewsets

from product.models import Product, ProductType
from ..serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.filter(is_public=True)
        product_type = self.request.query_params.get('type', None)
        count = self.request.query_params.get('count', None)

        # image_width = self.request.query_params.get('image_width', None)
        if product_type is not None:
            try:
                product_type_instance = ProductType.objects.filter(
                    name__icontains=product_type,
                ).first()
                queryset = queryset.filter(types=product_type_instance)
            except:
                pass
        # slide should happen after filtering
        if count:
            queryset = queryset[:int(count)]
        return queryset
