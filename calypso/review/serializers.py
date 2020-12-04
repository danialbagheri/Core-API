from .models import Review, Reply
from rest_framework import serializers


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()

    class Meta:
        model = Review
        exclude = ['customer_email', 'ip_address']


class ReviewCreateSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True,)
    name = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = '__all__'
