from rest_framework import serializers

from product.models import ProductType


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = (
            'id',
            'name',
        )
        read_only_fields = (
            'id',
            'name',
        )
