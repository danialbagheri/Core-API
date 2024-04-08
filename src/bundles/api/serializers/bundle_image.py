from rest_framework import serializers

from bundles.models import BundleImage


class BundleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundleImage
        fields = (
            'id',
            'image',
            'alternate_text',
            'image_type',
            'image_angle',
            'main',
            'secondary',
            'position',
        )
