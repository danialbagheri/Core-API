from django.contrib.sites.models import Site
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from web.models import Slider, SliderSlidesThroughModel


class SlideSerializer(serializers.ModelSerializer):
    desktop_resized = serializers.SerializerMethodField()
    desktop_webp = serializers.SerializerMethodField()
    mobile_webp = serializers.SerializerMethodField()

    def get_desktop_resized(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w', None)
        resize_h = request.query_params.get('resize_h', None)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = "1440"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.slide.lg_image:
            return domain + get_thumbnail(obj.slide.lg_image, f'{resize_w}{height}', quality=100, format="PNG").url

    def get_desktop_webp(self, obj):
        request = self.context.get("request")
        resize_w = request.query_params.get('resize_w', None)
        resize_h = request.query_params.get('resize_h', None)
        domain = Site.objects.get_current().domain
        if resize_h is None and resize_w is None:
            resize_w = "1440"
        if resize_w is None:
            resize_w = ""
        if resize_h is None:
            height = ""
        else:
            height = f"x{resize_h}"
        if obj.slide.lg_image:
            return domain + get_thumbnail(
                obj.slide.lg_image, f'{resize_w}{height}', quality=100, format="WEBP"
            ).url

    @staticmethod
    def get_mobile_webp(obj):
        domain = Site.objects.get_current().domain
        if obj.slide.sm_image:
            return domain + get_thumbnail(obj.slide.sm_image, f"640", quality=100, format="WEBP").url

    class Meta:
        model = SliderSlidesThroughModel
        fields = '__all__'
        depth = 2


class SliderSerializer(serializers.ModelSerializer):
    slider_slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Slider
        fields = '__all__'
        depth = 2
