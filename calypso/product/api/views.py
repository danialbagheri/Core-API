from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from calypso.common.permissions import WebhookPermission
from product.models import Product, ProductVariant, ProductType, Collection, ProductImage, Tag
from .serializers import (
    ProductVariantSerializer, ProductSerializer, ProductImageSerializer, TagSerializer, SingleProductSerializer,
    CollectionSerializer, ProductTypeSerializer
)
from ..tasks import ProductEditTask


class VariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = 'sku'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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
                    name__icontains=product_type).first()
                queryset = queryset.filter(types=product_type_instance)
            except:
                pass
        # slide should happen after filtering
        if count:
            queryset = queryset[: int(count)]
        return queryset


class SingleProductViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Product.objects.filter(is_public=True)
    serializer_class = SingleProductSerializer
    lookup_field = "slug"


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.all()
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


class ProductTypeListAPIView(ListAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()
    pagination_class = None


class FavoriteProductListAPIView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.favorite_products.filter(is_public=True)


class FavoriteProductUpdateAPIView(UpdateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.filter(is_public=True)
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        action = self.request.data.get('action', 'add')
        if action == 'add':
            user.favorite_products.add(product)
        elif action == 'remove':
            user.favorite_products.remove(product)
        else:
            return Response(
                data='Invalid action.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data='Action done successfully',
            status=status.HTTP_200_OK,
        )


class ProductEditWebhookAPI(APIView):
    permission_classes = (WebhookPermission,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        ProductEditTask().delay(request.data)
        return Response(data={}, status=status.HTTP_200_OK)
