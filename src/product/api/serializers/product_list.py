from bs4 import BeautifulSoup
from django.db.models import Avg
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from faq.serializers import FaqSerializer
from product.models import Product, ProductImage, CollectionItem
from product.utils import check_request_image_size_params
from . import ProductVariantSerializer, TagSerializer


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    faq_list = FaqSerializer(many=True, read_only=True, source='faqs')
    tags = TagSerializer(many=True, read_only=True)
    lowest_variant_price = serializers.ReadOnlyField()
    main_image = serializers.SerializerMethodField()
    secondary_image = serializers.SerializerMethodField()
    main_image_resized = serializers.SerializerMethodField()
    main_image_webp = serializers.SerializerMethodField()
    secondary_image_resized = serializers.SerializerMethodField()
    secondary_image_webp = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()
    total_review_count = serializers.SerializerMethodField()
    review_average_score = serializers.SerializerMethodField()
    collection_names = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    plain_description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = 'slug'
        depth = 3
        extra__kwargs = {'url': {'lookup_field': 'slug'}}

    @staticmethod
    def get_main_image(product: Product):
        if product.main_image:
            return f'https://service.calypsosun.com/media/{product.main_image.image.name}'

    @staticmethod
    def get_secondary_image(product: Product):
        if product.secondary_image:
            return f'https://service.calypsosun.com/media/{product.secondary_image.image.name}'

    def edit_image(self, image: ProductImage, image_format):
        request = self.context.get('request')
        resize_width, resize_height = check_request_image_size_params(request)
        if resize_height is None and resize_width is None:
            resize_width = '400'
        if resize_width is None:
            resize_width = ''
        if resize_height is None:
            height = ''
        else:
            height = f'x{resize_height}'
        image_url = image.image.url
        url = get_thumbnail(image_url, f'{resize_width}{height}', quality=100, format=image_format).url
        name = url.split('/media/')[1]
        return f'https://service.calypsosun.com/media/{name}'

    @staticmethod
    def _is_gif(image):
        if image.name.lower().endswith('.gif'):
            return True
        return False

    def get_main_image_resized(self, obj):
        if not obj.main_image or self._is_gif(obj.main_image.image):
            return
        return self.edit_image(obj.main_image, 'PNG')

    def get_main_image_webp(self, obj):
        if not obj.main_image or self._is_gif(obj.main_image.image):
            return
        return self.edit_image(obj.main_image, 'WEBP')

    def get_secondary_image_resized(self, product: Product):
        if not product.secondary_image or self._is_gif(product.secondary_image.image):
            return
        return self.edit_image(product.secondary_image, 'PNG')

    def get_secondary_image_webp(self, product: Product):
        if not product.secondary_image or self._is_gif(product.secondary_image.image):
            return
        return self.edit_image(product.secondary_image, 'WEBP')

    @staticmethod
    def get_total_review_count(obj):
        review_count = obj.review_set.filter(approved=True).count()
        return review_count

    @staticmethod
    def get_review_average_score(obj):
        average_score = obj.review_set.filter(
            approved=True).aggregate(Avg('score'))['score__avg']
        if average_score is not None:
            return f"{average_score:.1f}"
        return 0

    @staticmethod
    def get_collection_names(product: Product):
        return CollectionItem.objects.filter(
            collection_name__public=True,
            item=product,
        ).values_list('collection_name__name', flat=True)

    @staticmethod
    def get_types(product: Product):
        return list(product.types.all().values_list('name', flat=True))

    def get_is_favorite(self, product: Product):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.favorite_products.all().filter(id=product.id).exists()

    @staticmethod
    def get_plain_description(product: Product):
        if not product.description:
            return ''
        soup = BeautifulSoup(product.description)
        return soup.text
