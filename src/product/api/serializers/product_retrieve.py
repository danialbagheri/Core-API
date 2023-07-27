from django.db.models import Count
from rest_framework import serializers

from product.models import Product
from review.api.serializers import ReviewSerializer
from review.models import Review
from . import ProductSerializer, ProductReviewQuestionSerializer, ProductVariantSerializer, TagSerializer


class SingleProductSerializer(ProductSerializer):
    """
    Similar to ProductSerializer but with more info such as reviews and related_products,
    seperated for faster performance
    """
    questions = ProductReviewQuestionSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()
    score_chart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = "slug"
        depth = 3
        extra__kwargs = {'url': {'lookup_field': 'slug'}}

    @staticmethod
    def get_related_products(obj):
        related_products_filter = Product.objects.filter(
            tags__in=obj.tags.all(),
            is_public=True,
        ).exclude(id=obj.id).annotate(
            num_common_tags=Count('pk'),
        ).order_by('-num_common_tags')[:5]
        related_products = []
        for product in related_products_filter:
            main_image = product.main_image
            secondary_image = product.secondary_image
            related_products.append({
                'name': product.name,
                'slug': product.slug,
                'sub_title': product.sub_title,
                'main_image': main_image.image.url if main_image else None,
                'secondary_image': secondary_image.image.url if secondary_image else None,
                'img_height': f'{main_image.height if main_image else 0}',
                'img_width': f'{main_image.width if main_image else 0}',
                'secondary_image_height': secondary_image.height if secondary_image else 0,
                'secondary_image_width': secondary_image.width if secondary_image else 0,
                'total_review_count': product.get_total_review_count,
                'review_average_score': product.get_review_average_score,
                'starting_price': product.lowest_variant_price,
                'variants': ProductVariantSerializer(instance=product.variants.all(), many=True).data,
            })
        return related_products

    @staticmethod
    def get_reviews(product):
        review_instance = Review.objects.filter(product=product, approved=True)
        serializer = ReviewSerializer(
            many=True, read_only=True, instance=review_instance)
        return serializer.data

    @staticmethod
    def get_score_chart(product: Product):
        score_chart = {i: 0 for i in range(1, 6)}
        scores_data = Review.objects.filter(
            product=product,
            approved=True,
        ).values('score').annotate(score_count=Count('id'))
        for score_data in scores_data:
            score_chart[score_data['score']] = score_data['score_count']
        return score_chart
