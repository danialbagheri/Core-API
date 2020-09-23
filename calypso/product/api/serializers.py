from product.models import ProductCategory, Product, ProductImage
from rest_framework import serializers

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
    

class ProductSerializer(serializers.ModelSerializer):
    image_list = ProductImageSerializer(many=True, read_only=True, source='image')
    #shopify_information = serializers.ReadOnlyField()
    class Meta:
        model= Product
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
        depth = 2
        extra__kwargs = {'url': {'lookup_field': 'slug'}}