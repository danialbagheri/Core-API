from django.core.exceptions import ValidationError

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
        lookup_fields = 'pk'
