from rest_framework import serializers

from product.api.serializers import ProductImageSerializer
from product.models import ProductVariant


class SPFRecommendationVariantSerializer(serializers.ModelSerializer):
    image_list = ProductImageSerializer(many=True, read_only=True, source='variant_images')
    slug = serializers.SlugField(source='product.slug')
    review_average_score = serializers.FloatField(source='product.get_review_average_score')
    price = serializers.SerializerMethodField()
    compare_at_price = serializers.SerializerMethodField()
    euro_price = serializers.SerializerMethodField()
    euro_compare_at_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = (
            'id',
            'name',
            'sku',
            'image_list',
            'slug',
            'review_average_score',
            'price',
            'compare_at_price',
            'euro_price',
            'euro_compare_at_price',
        )

    @staticmethod
    def get_price(variant: ProductVariant):
        return '%.2f' % variant.price

    @staticmethod
    def get_compare_at_price(variant: ProductVariant):
        return '%.2f' % variant.compare_at_price if variant.compare_at_price else None

    @staticmethod
    def get_euro_price(variant: ProductVariant):
        return '%.2f' % variant.euro_price

    @staticmethod
    def get_euro_compare_at_price(variant: ProductVariant):
        return '%.2f' % variant.euro_compare_at_price if variant.euro_compare_at_price else None
