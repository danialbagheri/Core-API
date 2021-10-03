import base64

from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from review.models import ReviewImage
from review.utils import check_request_image_size_params, RESIZE_W


class ReviewImageSerializer(serializers.ModelSerializer):
    image_base64 = serializers.CharField(write_only=True)
    resized = serializers.SerializerMethodField()
    webp = serializers.SerializerMethodField()

    class Meta:
        model = ReviewImage
        fields = (
            'id',
            'image',
            'image_base64',
            'resized',
            'webp',
        )
        read_only_fields = (
            'id',
            'image',
            'resized',
            'webp',
        )

    def get_resized(self, obj):
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

    def create(self, validated_data):
        image_base64 = validated_data.pop('image_base64')
        image_format, image_str = image_base64.split(';base64,')
        extension = image_format.split('/')[-1]
        image = ContentFile(base64.b64decode(image_str), name='temp.' + extension)
        validated_data['image'] = image
        return super().create(validated_data)
