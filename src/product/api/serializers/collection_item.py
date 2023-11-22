from rest_framework import serializers

from . import SingleProductSerializer
from product.models import CollectionItem


class CollectionItemListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(item__is_public=True)
        return super().to_representation(data)


class CollectionItemSerializer(serializers.ModelSerializer):
    item = SingleProductSerializer(read_only=True)

    class Meta:
        model = CollectionItem
        fields = (
            'item',
        )
        list_serializer_class = CollectionItemListSerializer
        depth = 4
