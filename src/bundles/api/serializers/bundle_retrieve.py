from rest_framework import serializers

from bundles.models import Bundle, BundleItem
from bundles.services import BundlePriceProcessor
from .bundle_image import BundleImageSerializer
from .product import BundleItemProductSerializer
from .variant import BundleItemVariantSerializer


class BundleItemSerializer(serializers.ModelSerializer):
    product = BundleItemProductSerializer()
    variants = BundleItemVariantSerializer(many=True)

    class Meta:
        model = BundleItem
        fields = (
            'product',
            'quantity',
            'variants',
            'position',
        )


class BundleRetrieveSerializer(serializers.ModelSerializer):
    items = BundleItemSerializer(many=True)
    images = BundleImageSerializer(many=True)
    compare_at_price = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    euro_compare_at_price = serializers.SerializerMethodField()
    euro_final_price = serializers.SerializerMethodField()

    class Meta:
        model = Bundle
        fields = (
            'id',
            'description',
            'items',
            'images',
            'compare_at_price',
            'final_price',
            'euro_compare_at_price',
            'euro_final_price',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bundle_price_processor = BundlePriceProcessor(self.instance)
        self.bundle_price_processor.process_bundle_price()

    def get_compare_at_price(self, bundle: Bundle):
        return self.bundle_price_processor.compare_at_price

    def get_final_price(self, bundle: Bundle):
        return self.bundle_price_processor.final_price

    def get_euro_compare_at_price(self, bundle: Bundle):
        return self.bundle_price_processor.euro_compare_at_price

    def get_euro_final_price(self, bundle: Bundle):
        return self.bundle_price_processor.euro_final_price
