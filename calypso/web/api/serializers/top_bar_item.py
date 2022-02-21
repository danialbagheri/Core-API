from rest_framework import serializers

from web.models import TopBarItem


class TopBarItemListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        data = data.filter(is_active=True).order_by('position')
        return super().to_representation(data)


class TopBarItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBarItem
        list_serializer_class = TopBarItemListSerializer
        fields = (
            'id',
            'text',
            'icon',
            'url',
            'position',
        )
