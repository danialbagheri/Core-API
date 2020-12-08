from product.models import Product, ProductVariant, ProductType, Collection, ProductImage, IMAGE_TYPE
from review.models import Review, Reply
from rest_framework import viewsets
from .serializers import ProductVariantSerializer, ProductSerializer, ProductImageSerializer



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
        collection = self.request.query_params.get('collection', None)
        if product_type is not None:
            try:
                product_type_instance = ProductType.objects.filter(
                    name__icontains=product_type).first()
                queryset = queryset.filter(types=product_type_instance)
            except:
                pass
        if collection is not None:
            collection_instance = Collection.objects.filter(
                name__icontains=collection).first()
            queryset = queryset.filter(collections=collection_instance)
        if top_seller and top_seller.lower() == "yes":
            queryset = queryset.filter(top_seller=True)
        # slide should happen after filtering
        if count:
            queryset = queryset[: int(count)]
        return queryset


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
        count=0
        for i in IMAGE_TYPE:
            if str(query).lower() in i[1].lower():
                return IMAGE_TYPE[count][0]
            count += 1
        return None