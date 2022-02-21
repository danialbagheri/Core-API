from rest_framework import serializers

from web.api.serializers.top_bar_item import TopBarItemSerializer
from web.models import TopBar


class TopBarListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        data = data.filter(is_active=True).order_by('position')
        return super().to_representation(data)


class TopBarSerializer(serializers.ModelSerializer):
    items = TopBarItemSerializer(many=True, read_only=True)

    class Meta:
        model = TopBar
        list_serializer_class = TopBarListSerializer
        fields = (
            'id',
            'name',
            'position',
        )
