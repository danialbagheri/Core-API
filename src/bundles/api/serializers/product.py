from bs4 import BeautifulSoup
from rest_framework import serializers

from faq.serializers import FaqSerializer
from product.api.serializers import TagSerializer
from product.models import Product
from .variant import BundleItemVariantSerializer


class BundleItemProductSerializer(serializers.ModelSerializer):
    variants = BundleItemVariantSerializer(many=True)
    faqs = FaqSerializer(many=True)
    tags = TagSerializer(many=True)
    plain_description = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    secondary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'sub_title',
            'direction_of_use',

            'plain_description',
            'main_image',
            'secondary_image',
            'variants',
            'faqs',
            'tags',
        )

    @staticmethod
    def get_plain_description(product: Product):
        if not product.description:
            return ''
        soup = BeautifulSoup(product.description, parser='html.parser')
        return soup.text

    @staticmethod
    def get_main_image(product: Product):
        if product.main_image:
            return product.main_image.image.url

    @staticmethod
    def get_secondary_image(product: Product):
        if product.secondary_image:
            return product.secondary_image.image.url
