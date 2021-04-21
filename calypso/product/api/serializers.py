from product.models import ProductVariant, Product, ProductImage, WhereToBuy, Tag
from review.models import Review, Reply
from rest_framework import serializers
from review.serializers import ReviewSerializer
from faq.serializers import FaqSerializer
from sorl.thumbnail import get_thumbnail
from django.contrib.sites.models import Site
from django.core.serializers import json

class WhereToBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = WhereToBuy
        fields = ('id', 'url', 'stockist')
        depth = 2
        # lookup_field = 'product'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class ProductImageSerializer(serializers.ModelSerializer):
    resized = serializers.SerializerMethodField()
    webp = serializers.SerializerMethodField()
    def get_resized(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w',None)
        resize_h = request.query_params.get('resize_h',None)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = "100"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.image:
            return domain+get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format="PNG").url
    
    def get_webp(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w',None)
        resize_h = request.query_params.get('resize_h',None)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = "100"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.image:
            return domain+get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format="WEBP").url
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    image_list = ProductImageSerializer(
        many=True, read_only=True, source='variant_images')
    where_to_buy = WhereToBuySerializer(
        many=True, read_only=True, source='wheretobuy')

    class Meta:
        model = ProductVariant
        fields = '__all__'
        lookup_field = "sku"
        extra__kwargs = {'url': {'lookup_field': 'sku'}}


class ProductSerializer(serializers.ModelSerializer):
    main_image_resized =serializers.SerializerMethodField()
    main_image_webp =serializers.SerializerMethodField()
    variants = ProductVariantSerializer(many=True, read_only=True)
    main_image = serializers.ReadOnlyField()
    lowest_variant_price = serializers.ReadOnlyField()
    faq_list = FaqSerializer(many=True, read_only=True, source='faqs') 
    total_review_count = serializers.SerializerMethodField()
    review_average_score = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = "slug"
        depth = 3
        extra__kwargs = {'url': {'lookup_field': 'slug'}}
    
    def get_main_image_resized(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w',None)
        resize_h = request.query_params.get('resize_h',None)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = "400"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.main_image:
            return domain+get_thumbnail(obj.main_image, f'{resize_w}{height}', quality=100, format="PNG").url

    def get_main_image_webp(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w',None)
        resize_h = request.query_params.get('resize_h',None)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = "400"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.main_image:
            return domain+get_thumbnail(obj.main_image, f'{resize_w}{height}', quality=100, format="WEBP").url
    
    def get_total_review_count(self, obj):
        review_count = obj.review_set.filter(approved=True).count()
        return review_count
    
    def get_review_average_score(self, obj):
        score = 0
        for review in obj.review_set.all():
            score += review.score
        try:
            average_score = score / self.get_total_review_count(obj)
            return average_score
        except ZeroDivisionError:
            return 0

class RelatedProducts(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SingleProductSerializer(ProductSerializer):
    '''
    Similar to ProductSerializer but with more info such as reviews and related_products, 
    seperated for faster performance
    '''
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    related_products = serializers.SerializerMethodField()
    # related_products = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = "slug"
        depth = 3
        extra__kwargs = {'url': {'lookup_field': 'slug'}}
    
    def get_related_products(self, obj):
        related_products_filter = Product.objects.filter(tags__in=obj.tags.all()).exclude(id=obj.id)[:5]
        # related_products_fields = related_products_filter.values('name', 'slug', 'sub_title')
        related_products = []
        for product in related_products_filter:
            related_products.append({
                "name": product.name,
                "slug": product.slug,
                "sub_title": product.sub_title,
                "main_image": product.main_image,
                "starting_price": product.lowest_variant_price
            })
        return related_products
