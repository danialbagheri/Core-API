from django.db.models import F
from rest_framework import serializers

from product.models import ProductVariant
from product.services import VariantPriceRepresentative, VariantIngredientsRepresentative
from web.api.serializers import InstagramSerializer
from . import ProductImageSerializer, WhereToBuySerializer


class ProductVariantListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        if not hasattr(data, 'filter'):
            return super().to_representation(data)
        data = data.filter(is_public=True).order_by(F('position').asc(nulls_last=True))
        return super().to_representation(data)


class ProductVariantSerializer(serializers.ModelSerializer):
    image_list = ProductImageSerializer(many=True, read_only=True, source='variant_images')
    where_to_buy = WhereToBuySerializer(many=True, read_only=True, source='wheretobuy')
    price_per_100ml = serializers.SerializerMethodField()
    instagram_posts = InstagramSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    compare_at_price = serializers.SerializerMethodField()
    euro_price = serializers.SerializerMethodField()
    euro_compare_at_price = serializers.SerializerMethodField()
    euro_price_per_100ml = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductVariant
        fields = '__all__'
        list_serializer_class = ProductVariantListSerializer
        lookup_field = 'sku'
        extra__kwargs = {'url': {'lookup_field': 'sku'}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variant_price_representative = VariantPriceRepresentative()

    def get_price(self, variant: ProductVariant):
        return self.variant_price_representative.get_price(variant)

    def get_compare_at_price(self, variant: ProductVariant):
        return self.variant_price_representative.get_compare_at_price(variant)

    def get_price_per_100ml(self, variant: ProductVariant):
        return self.variant_price_representative.get_price_per_100ml(variant)

    def get_euro_price(self, variant: ProductVariant):
        return self.variant_price_representative.get_euro_price(variant)

    def get_euro_compare_at_price(self, variant: ProductVariant):
        return self.variant_price_representative.get_euro_compare_at_price(variant)

    def get_euro_price_per_100ml(self, variant: ProductVariant):
        return self.variant_price_representative.get_euro_price_per_100ml(variant)

    @staticmethod
    def get_ingredients(variant: ProductVariant):
        return VariantIngredientsRepresentative(variant).get_ingredients()

    def get_is_favorite(self, variant: ProductVariant):
        if 'request' not in self.context:
            return False
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.favorite_variants.all().filter(id=variant.id).exists()
