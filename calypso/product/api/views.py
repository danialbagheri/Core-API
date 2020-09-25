from product.models import ProductCategory, Product, ProductType
from review.models import Review, Reply
from rest_framework import viewsets
from .serializers import ProductSerializer, ProductCategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "product_code"


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = ProductCategory.objects.all()
        product_type = self.request.query_params.get('type', None)
        if product_type is not None:
            try:
                product_type_instance = ProductType.objects.get(
                    name=product_type)
                queryset = queryset.filter(types=product_type_instance)
            except:
                pass
        return queryset
