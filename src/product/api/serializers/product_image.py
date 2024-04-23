from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from product.models import ProductImage
from product.utils import check_request_image_size_params, RESIZE_W


class ProductImageListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        data = data.filter(is_public=True).order_by('-main', '-secondary')
        return super().to_representation(data)


class ProductImageSerializer(serializers.ModelSerializer):
    resized = serializers.SerializerMethodField()
    webp = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        list_serializer_class = ProductImageListSerializer
        fields = (
            'id',
            'name',
            'updated',
            'image',
            'image_type',
            'image_angle',
            'alternate_text',
            'height',
            'width',
            'main',
            'secondary',
            'resized',
            'webp',
        )

    @staticmethod
    def _is_gif(image):
        if image.name.lower().endswith('.gif'):
            return True
        return False

    def get_resized(self, obj):
        if self._is_gif(obj.image):
            return None

        request = self.context.get("request")
        resize_w, resize_h = check_request_image_size_params(request)
        if resize_h is None and resize_w is None:
            resize_w = RESIZE_W
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.image:
            return get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format="PNG").url

    def get_webp(self, obj):
        if self._is_gif(obj.image):
            return None

        request = self.context.get("request")
        resize_w, resize_h = check_request_image_size_params(request)
        if resize_h is None and resize_w is None:
            resize_w = "100"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.image:
            return get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format="WEBP").url
