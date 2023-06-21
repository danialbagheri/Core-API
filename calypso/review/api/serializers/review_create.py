from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from product.models import Product
from . import ReplySerializer, ReviewImageSerializer
from ...models import Review, ReviewImage, ReviewAnswer
from ...services import ReviewNotificationEmail


class ReviewCreateSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()
    image_ids = serializers.ListField(write_only=True, required=False)
    answers = serializers.ListField(write_only=True, required=False)
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, attrs):
        if not self.context['slug']:
            raise ValidationError('Product slug is not set.')
        return super().validate(attrs)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    @staticmethod
    def create_review_answers(answers, review):
        for answer in answers:
            ReviewAnswer.objects.create(
                question_id=answer['question_id'],
                review=review,
                text=answer['answer'],
            )

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
        image_ids = validated_data.pop('image_ids', [])
        answers = validated_data.pop('answers', [])
        request = self.context['request']
        product_slug = self.context['slug']
        product_instance = get_object_or_404(Product, slug=product_slug)
        user_source = request.META.get("HTTP_REFERER", "")
        user_ip = self.get_client_ip(request=request)
        validated_data.update({
            'product': product_instance,
            'ip_address': user_ip,
            'source': user_source,
        })
        review = super().create(validated_data)
        ReviewImage.objects.filter(
            id__in=image_ids,
        ).update(review=review)
        self.create_review_answers(answers, review)
        ReviewNotificationEmail(review).send_email()
        return review
