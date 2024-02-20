from django.db.models import F
from rest_framework import serializers

from product.models import ProductVariant, VariantIngredientThrough
from product.utils import get_ml_number
from web.api.serializers import InstagramSerializer
from . import ProductImageSerializer, WhereToBuySerializer


class ProductVariantListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
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
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = '__all__'
        list_serializer_class = ProductVariantListSerializer
        lookup_field = 'sku'
        extra__kwargs = {'url': {'lookup_field': 'sku'}}

    @staticmethod
    def get_price_per_100ml(variant: ProductVariant):
        if not variant.size:
            return None
        ml_number = get_ml_number(variant.size)
        return '%.2f' % (100 * (variant.price / ml_number))

    @staticmethod
    def get_price(variant: ProductVariant):
        return '%.2f' % variant.price

    @staticmethod
    def get_compare_at_price(variant: ProductVariant):
        return '%.2f' % variant.compare_at_price if variant.compare_at_price else None

    @staticmethod
    def get_euro_price(variant: ProductVariant):
        return '%.2f' % variant.euro_price if variant.euro_price else None

    @staticmethod
    def get_euro_compare_at_price(variant: ProductVariant):
        return '%.2f' % variant.euro_compare_at_price if variant.euro_compare_at_price else None

    @staticmethod
    def get_ingredients(variant: ProductVariant):
        if not VariantIngredientThrough.objects.exists():
            return list(variant.ingredients.all().values_list('name', flat=True))
        variant_ingredients = VariantIngredientThrough.objects.filter(
            variant=variant,
        ).select_related('ingredient').order_by('priority')
        ingredient_names = [variant_ingredient.ingredient.name for variant_ingredient in variant_ingredients]
        return ingredient_names
