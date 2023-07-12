from rest_framework import serializers

from . import SingleProductSerializer
from product.models import CollectionItem


class CollectionItemSerializer(serializers.ModelSerializer):
    item = SingleProductSerializer(read_only=True)

    class Meta:
        model = CollectionItem
        fields = (
            'item',
        )
        depth = 4
