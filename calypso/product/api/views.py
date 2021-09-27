from rest_framework import viewsets

from product.models import Product, ProductVariant, ProductType, Collection, ProductImage, Tag
from .serializers import (
    ProductVariantSerializer, ProductSerializer, ProductImageSerializer, TagSerializer, SingleProductSerializer,
    CollectionSerializer
)


class VariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = "sku"


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.all()
        product_type = self.request.query_params.get('type', None)
        count = self.request.query_params.get('count', None)
        top_seller = self.request.query_params.get('top', None)

        # image_width = self.request.query_params.get('image_width', None)
        if product_type is not None:
            try:
                product_type_instance = ProductType.objects.filter(
                    name__icontains=product_type).first()
                queryset = queryset.filter(types=product_type_instance)
            except:
                pass
        if top_seller and top_seller.lower() == "yes":
            queryset = queryset.filter(top_seller=True)
        # slide should happen after filtering
        if count:
            queryset = queryset[: int(count)]
        return queryset


class SingleProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = SingleProductSerializer
    lookup_field = "slug"


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.filter(public=True)
    serializer_class = CollectionSerializer
    lookup_field = "slug"


class ProductImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    lookup_field = "variant_sku"

    def get_queryset(self):
        queryset = ProductImage.objects.all()
        image_type = self.request.query_params.get('image_type', None)
        sku= self.request.query_params.get('sku', None)
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
