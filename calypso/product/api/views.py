from product.models import Product, ProductVariant, ProductType
from review.models import Review, Reply
from rest_framework import viewsets
from .serializers import ProductVariantSerializer, ProductSerializer


class VariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = "sku"


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.all()
        product_type = self.request.query_params.get('type', None)
        count = self.request.query_params.get('count', None)
        top_seller = self.request.query_params.get('top', None)
        if product_type is not None:
            try:
                product_type_instance = ProductType.objects.get(
                    name=product_type)
                queryset = queryset.filter(types=product_type_instance)
            except:
                pass
        if top_seller and top_seller.lower() == "yes":
            queryset = queryset.filter(top_seller=True)
        # slide should happen after filtering
        if count:
            queryset = queryset[: int(count)]
        return queryset
