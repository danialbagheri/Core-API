from django.contrib.sites.models import Site
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from web.models import Slider, SliderSlidesThroughModel, Slide


class SlideSerializer(serializers.ModelSerializer):
    desktop_resized = serializers.SerializerMethodField()
    desktop_webp = serializers.SerializerMethodField()
    mobile_webp = serializers.SerializerMethodField()

    image_png = serializers.SerializerMethodField()
    image_webp = serializers.SerializerMethodField()

    def _get_image(self, slide: Slide):
        request = self.context['request']
        image_type = request.query_params.get('image_type')
        if not image_type:
            return None
        if image_type == 'xs':
            return slide.xs_image
        elif image_type == 'sm':
            return slide.sm_image
        elif image_type == 'md':
            return slide.md_image
        elif image_type == 'lg':
            return slide.lg_image
        elif image_type == 'xl':
            return slide.xl_image

    def _create_thumbnail(self, image, image_format):
        if not image:
            return None
        request = self.context['request']
        resize_w = request.query_params.get('resize_w')
        resize_h = request.query_params.get('resize_h')
        if not resize_w or not resize_h:
            return None
        domain = Site.objects.get_current().domain
        return domain + get_thumbnail(image, f'{resize_w}x{resize_h}', quality=100, format=image_format).url

    def get_image_png(self, instance: SliderSlidesThroughModel):
        slide = instance.slide
        image = self._get_image(slide)
        return self._create_thumbnail(image, 'PNG')

    def get_image_webp(self, instance: SliderSlidesThroughModel):
        slide = instance.slide
        image = self._get_image(slide)
        return self._create_thumbnail(image, 'WEBP')

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
