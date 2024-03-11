from rest_framework import viewsets

from product.models import ProductVariant, ProductImage
from ..serializers import ProductImageSerializer


class ProductImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductImage.objects.filter(is_public=True)
    serializer_class = ProductImageSerializer
    lookup_field = 'variant_sku'

    def get_queryset(self):
        queryset = ProductImage.objects.filter(is_public=True)
        image_type = self.request.query_params.get('image_type', None)
        sku = self.request.query_params.get('sku', None)
        if image_type is not None:
            try:
                image_type_tuple = self.get_product_image_type_tuple_search(image_type)
                queryset = queryset.filter(image_type__icontains=image_type_tuple)
            except:
                pass
        if sku is not None:
            try:
                product_variant_instance = ProductVariant.objects.filter(sku=sku).first()
                queryset = queryset.filter(variant=product_variant_instance)
            except:
                pass
        return queryset

    def get_product_image_type_tuple_search(self, query):
        count = 0
        for i in ProductImage.IMAGE_TYPE:
            if str(query).lower() in i[1].lower():
                return ProductImage.IMAGE_TYPE[count][0]
            count += 1
        return
