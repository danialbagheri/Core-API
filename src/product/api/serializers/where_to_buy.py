from rest_framework import serializers

from product.models import WhereToBuy


class WhereToBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = WhereToBuy
        fields = (
            'id',
            'url',
            'stockist',
        )
        depth = 2
