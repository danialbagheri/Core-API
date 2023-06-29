from rest_framework import serializers

from web.models import InstagramPost


class InstagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramPost
        fields = (
            'id',
            'instagram_id',
            'media_type',
            'media_url',
            'thumbnail',
            'webp',
            'caption',
            'permalink',
        )
