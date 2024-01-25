from django.db.models import F
from rest_framework import serializers

from product.api.serializers import ProductImageSerializer, WhereToBuySerializer
from product.models import ProductVariant
from product.services import VariantPriceRepresentative, VariantIngredientsRepresentative


class BundleItemVariantListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        data = data.filter(is_public=True).order_by(F('position').asc(nulls_last=True))
        return super().to_representation(data)


class BundleItemVariantSerializer(serializers.ModelSerializer):
    image_list = ProductImageSerializer(many=True, read_only=True, source='variant_images')
    where_to_buy = WhereToBuySerializer(many=True, read_only=True, source='wheretobuy')
    price = serializers.SerializerMethodField()
    compare_at_price = serializers.SerializerMethodField()
    price_per_100ml = serializers.SerializerMethodField()
    euro_price = serializers.SerializerMethodField()
    euro_compare_at_price = serializers.SerializerMethodField()
    euro_price_per_100ml = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = (
            'sku',
            'name',
            'shopify_storefront_variant_id',
            'barcode',
            'date_first_available',
            'claims',
            'discontinued',
            'size',
            'rrp',
            'inventory_quantity',
            'price',
            'compare_at_price',
            'price_per_100ml',
            'euro_price',
            'euro_compare_at_price',
            'euro_price_per_100ml',
            'ingredients',
            'image_list',
            'where_to_buy',
        )
        list_serializer_class = BundleItemVariantListSerializer

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
