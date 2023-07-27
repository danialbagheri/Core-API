import base64

import requests
from rest_framework import serializers

from product.models import Tag


class TagSerializer(serializers.ModelSerializer):
    svg_icon_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = (
            'id',
            'icon',
            'svg_icon',
            'svg_icon_base64',
            'name',
            'slug',
        )

    @staticmethod
    def get_svg_icon_base64(tag: Tag):
        svg_icon = tag.svg_icon
        if not svg_icon:
            return None

        response = requests.get(svg_icon.url)
        svg_contents = response.content
        encoded_svg = base64.b64encode(svg_contents).decode('utf-8')
        data_uri = 'data:image/svg+xml;base64,' + encoded_svg
        return data_uri
