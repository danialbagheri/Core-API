from django.contrib.sites.models import Site
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from product.models import ProductImage
from product.utils import check_request_image_size_params, RESIZE_W


class ProductImageSerializer(serializers.ModelSerializer):
    resized = serializers.SerializerMethodField()
    webp = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = '__all__'

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
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = RESIZE_W
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.image:
            return domain+get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format="PNG").url

    def get_webp(self, obj):
        if self._is_gif(obj.image):
            return None

        request = self.context.get("request")
        resize_w, resize_h = check_request_image_size_params(request)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = "100"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.image:
            return domain+get_thumbnail(obj.image, f'{resize_w}{height}', quality=100, format="WEBP").url
