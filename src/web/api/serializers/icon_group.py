from rest_framework import serializers

from web.models import IconGroupItem, IconGroup


class IconGroupItemListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        data = data.filter(is_active=True)
        return super().to_representation(data)


class IconGroupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconGroupItem
        list_serializer_class = IconGroupItemListSerializer
        fields = (
            'id',
            'name',
            'icon',
            'svg_icon',
            'svg_icon_text',
            'url',
            'position',
        )


class IconGroupSerializer(serializers.ModelSerializer):
    items = IconGroupItemSerializer(many=True, read_only=True)

    class Meta:
        model = IconGroup
        fields = (
            'id',
            'name',
            'items',
        )
