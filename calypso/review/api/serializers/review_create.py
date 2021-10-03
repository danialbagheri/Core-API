from django.core.exceptions import ValidationError
from django.core.mail import mail_managers, mail_admins
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from product.models import Product
from . import ReplySerializer, ReviewImageSerializer
from ...models import Review, ReviewImage


class ReviewCreateSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()
    image_ids = serializers.ListField(write_only=True)
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
    def notify_the_admin(review, product_name):
        subject = f"A new review has been submitted on {review.source}"
        message = f"""
            Please check and approve the latest review by visiting https://service.calypsosun.com/dashboard/reviews/{review.id}/
            user ip: {review.ip_address}
            Product: {product_name}
            Subject: {review.title}
            Review:
            {review.comment}
            """
        try:
            mail_managers(subject, message)
        except Exception as e:
            mail_admins("New Review Email notification failed", f"{e}")

    def create(self, validated_data):
        image_ids = validated_data.pop('image_ids', [])
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
        self.notify_the_admin(
            review=review,
            product_name=product_instance.name,
        )
        return review