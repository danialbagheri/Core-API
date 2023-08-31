from rest_framework import serializers

from product.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'icon',
            'svg_icon',
            'name',
            'slug',
        )
