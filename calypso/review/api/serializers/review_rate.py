from django.core.exceptions import ValidationError
from rest_framework import serializers

from review.models import Review, ReviewRate


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
