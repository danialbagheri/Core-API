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
        data = data.filter(is_public=True).order_by(F('position').asc(nulls_last=True))
        return super().to_representation(data)


class ProductVariantSerializer(serializers.ModelSerializer):
    image_list = ProductImageSerializer(
        many=True, read_only=True, source='variant_images')
    where_to_buy = WhereToBuySerializer(
        many=True, read_only=True, source='wheretobuy')
    instagram_posts = InstagramSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    compare_at_price = serializers.SerializerMethodField()
    price_per_100ml = serializers.SerializerMethodField()
    euro_price = serializers.SerializerMethodField()
    euro_compare_at_price = serializers.SerializerMethodField()
    euro_price_per_100ml = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = '__all__'
        list_serializer_class = ProductVariantListSerializer
        lookup_field = 'sku'
        extra__kwargs = {'url': {'lookup_field': 'sku'}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variant_price_representative = VariantPriceRepresentative(self.instance)

    def get_price(self, _):
        return self.variant_price_representative.get_price()

    def get_compare_at_price(self, _):
        return self.variant_price_representative.get_compare_at_price()

    def get_price_per_100ml(self, _):
        return self.variant_price_representative.get_price_per_100ml()

    def get_euro_price(self, _):
        return self.variant_price_representative.get_euro_price()

    def get_euro_compare_at_price(self, _):
        return self.variant_price_representative.get_euro_compare_at_price()

    def get_euro_price_per_100ml(self, _):
        return self.variant_price_representative.get_euro_price_per_100ml()

    @staticmethod
    def get_ingredients(variant: ProductVariant):
        return VariantIngredientsRepresentative(variant).get_ingredients()
