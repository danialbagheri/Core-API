from rest_framework import serializers

from product.models import ProductType
from web.api.serializers import SliderSerializer


class ProductTypeSerializer(serializers.ModelSerializer):
    slider = SliderSerializer(read_only=True)

    class Meta:
        model = ProductType
        fields = (
            'id',
            'name',
            'slug',
            'slider',
        )
