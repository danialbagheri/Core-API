from product.models import ProductVariant, Product, ProductImage, WhereToBuy, Tag, Collection, CollectionItem
from review.models import Review, Reply
from rest_framework import serializers
from review.serializers import ReviewSerializer
from faq.serializers import FaqSerializer
from sorl.thumbnail import get_thumbnail
from django.contrib.sites.models import Site
from django.core.serializers import json
from django.db.models import Avg, Count

RESIZE_W = 100
RESIZE_H = 100


def check_request_image_size_params(request):
    if request and request.query_params:
        resize_w = request.query_params.get('resize_w', None)
        resize_h = request.query_params.get('resize_h', None)
        return resize_w, resize_h
    else:
        return None, None


class WhereToBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = WhereToBuy
        fields = ('id', 'url', 'stockist')
        depth = 2


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class ProductImageSerializer(serializers.ModelSerializer):
    resized = serializers.SerializerMethodField()
    webp = serializers.SerializerMethodField()

    def get_resized(self, obj):
        request = self.context.get("request")
        resize_w, resize_h = check_request_image_size_params(request)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = RESIZE_W
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
        resize_w, resize_h = check_request_image_size_params(request)
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
    main_image_resized = serializers.SerializerMethodField()
    main_image_webp = serializers.SerializerMethodField()
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
        resize_w, resize_h = check_request_image_size_params(request)
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
        resize_w, resize_h = check_request_image_size_params(request)
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

        average_score = obj.review_set.filter(
            approved=True).aggregate(Avg('score'))['score__avg']
        if average_score != None:
            return f"{average_score:.1f}"
        else:
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
    reviews = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    # related_products = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = "slug"
        depth = 3
        extra__kwargs = {'url': {'lookup_field': 'slug'}}

    def get_related_products(self, obj):
        # related_products_filter = Product.objects.filter(
        #     tags__in=obj.tags.all()).exclude(id=obj.id)[:5]
        related_products_filter = Product.objects.filter(tags__in=obj.tags.all()).exclude(id=obj.id).\
            annotate(num_common_tags=Count('pk')).order_by(
                '-num_common_tags')[:5]
        # related_products_fields = related_products_filter.values('name', 'slug', 'sub_title')
        related_products = []
        for product in related_products_filter:
            # import pdb
            # pdb.set_trace()
            related_products.append({
                "name": product.name,
                "slug": product.slug,
                "sub_title": product.sub_title,
                "main_image": product.main_image,
                # "main_image": ProductImageSerializer(product.main_image_object),
                "img_height": f"{product.main_image_object.height if product.main_image_object else 0}",
                "img_width": f"{product.main_image_object.width if product.main_image_object else 0}",
                "total_review_count": product.get_total_review_count,
                "review_average_score": product.get_review_average_score,
                "starting_price": product.lowest_variant_price
            })
        return related_products

    def get_reviews(self, obj):
        review_instance = Review.objects.filter(product=obj, approved=True)
        serializer = ReviewSerializer(
            many=True, read_only=True, instance=review_instance)
        return serializer.data


class CollectionItemSerializer(serializers.ModelSerializer):
    item = SingleProductSerializer(read_only=True)

    class Meta:
        model = CollectionItem
        fields = ('item',)
        depth = 4


class CollectionSerializer(serializers.ModelSerializer):
    # items = serializers.SerializerMethodField()
    items = CollectionItemSerializer(many=True, source="collection_items")
    counts = serializers.SerializerMethodField()

    def get_items(self, obj):
        items = [n.item for n in obj.collection_items.all()]
        request = self.context.get("request")
        return ProductSerializer(context={'request': request}, instance=items, many=True).data

    def get_counts(self, obj):
        return obj.collection_items.count()

    class Meta:
        model = Collection
        fields = '__all__'
        depth = 4
