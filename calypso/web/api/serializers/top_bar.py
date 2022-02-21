from rest_framework import serializers

from web.api.serializers.top_bar_item import TopBarItemSerializer
from web.models import TopBar


class TopBarSerializer(serializers.ModelSerializer):
    items = TopBarItemSerializer(many=True, read_only=True)

    class Meta:
        model = TopBar
        fields = (
            'id',
            'name',
            'position',
            'items',
        )
