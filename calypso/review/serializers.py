from django.core.exceptions import ValidationError
from django.core.mail import mail_managers, mail_admins
from django.shortcuts import get_object_or_404

from product.models import Product
from .models import Review, Reply, ReviewRate
from rest_framework import serializers, pagination
from rest_framework.response import Response


class ReviewPagination(pagination.PageNumberPagination):
    total = 12

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_review_count': len(data) + 1,
            'review_average_score': self.get_total_review_score(data),
            'results': data
        })

    def get_total_review_score(self, data):
        review_count = len(data)
        score = 0
        for review in data:
            score += review['score']
        try:
            total_score = score / review_count
            return total_score
        except ZeroDivisionError:
            return 0


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()
    helpful = serializers.ReadOnlyField()

    class Meta:
        model = Review
        exclude = ['customer_email', 'ip_address']


class ReviewRateSerializer(serializers.ModelSerializer):
    rate_type = serializers.CharField(write_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'like',
            'dislike',
            'rate_type',
        )
        read_only_fields = (
            'id',
            'like',
            'dislike',
        )

    def validate(self, attrs):
        cookie = self.context['cookie']
        if cookie and ReviewRate.objects.filter(
            user_cookie=cookie,
            review_id=self.instance.id,
        ).exists():
            raise ValidationError('User already rated this review.')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        rate_type = validated_data.pop('rate_type')
        if rate_type == 'like':
            validated_data['like'] = instance.like + 1
        elif rate_type == 'dislike':
            validated_data['dislike'] = instance.dislike + 1
        cookie = self.context['cookie']
        if cookie:
            ReviewRate.objects.create(
                review=instance,
                rate_type=rate_type,
                user_cookie=cookie,
            )
        return super().update(instance, validated_data)


class ReviewCreateSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()

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
            Please check the latest review by visiting https://service.calypsosun.com/dashboard/reviews/{review.id}/
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
        self.notify_the_admin(
            review=review,
            product_name=product_instance.name,
        )
        return review
