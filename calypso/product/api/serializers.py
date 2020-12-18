from product.models import ProductVariant, Product, ProductImage, WhereToBuy
from review.models import Review, Reply
from rest_framework import serializers
from review.serializers import ReviewSerializer

class WhereToBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = WhereToBuy
        fields = ('id', 'url', 'stockist')
        depth = 2
        # lookup_field = 'product'


class ProductImageSerializer(serializers.ModelSerializer):
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
    variants = ProductVariantSerializer(many=True, read_only=True)
    main_image = serializers.ReadOnlyField()
    lowest_variant_price = serializers.ReadOnlyField()
    # reviews = ReviewSerializer(many=True, read_only=True, source='review_set') #only enable if you need to see full review list
    total_review_count = serializers.SerializerMethodField()
    review_average_score = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = "slug"
        depth = 3
        extra__kwargs = {'url': {'lookup_field': 'slug'}}
    
    def get_total_review_count(self, obj):
        review_count = obj.review_set.count()
        return review_count
    
    def get_review_average_score(self, obj):
        score = 0
        for review in obj.review_set.all():
            score += review.score
        # import pdb; pdb.set_trace()
        try:
            average_score = score / self.get_total_review_count(obj)
            return average_score
        except ZeroDivisionError:
             return 0
        
