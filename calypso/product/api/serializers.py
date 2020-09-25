from product.models import ProductCategory, Product, ProductImage, WhereToBuy
from review.models import Review, Reply
from rest_framework import serializers


class WhereToBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = WhereToBuy
        fields = ('id', 'url', 'stockist')
        depth = 2
        # lookup_field = 'product'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image_list = ProductImageSerializer(
        many=True, read_only=True, source='image')
    where_to_buy = WhereToBuySerializer(
        many=True, read_only=True, source='wheretobuy')

    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = "product_code"
        extra__kwargs = {'url': {'lookup_field': 'product_code'}}


class ProductCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    main_image = serializers.ReadOnlyField()
    lowest_variant_price = serializers.ReadOnlyField()

    class Meta:
        model = ProductCategory
        fields = '__all__'
        lookup_field = "slug"
        depth = 3
        extra__kwargs = {'url': {'lookup_field': 'slug'}}
