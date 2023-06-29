from rest_framework import serializers

from . import ReplySerializer, ReviewImageSerializer
from ...models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()
    helpful = serializers.ReadOnlyField()
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        exclude = ['customer_email', 'ip_address']
