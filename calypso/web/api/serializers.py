import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from ipware import get_client_ip
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from web.models import Slider, SliderSlidesThroughModel, Configuration

REASON_CHOICES = [
    'Urgent: Change Order detail or Address',
    'Question about order or Delivery',
    'Press Contact & Media',
    'Wholesale, Discount, promo code query',
    'Product Question',
    'Other'
]


class ContactFormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=200)
    subject = serializers.CharField(max_length=200, required=False)
    reason = serializers.ChoiceField(choices=REASON_CHOICES,)
    message = serializers.CharField()

    def to_internal_value(self, data):
        if 'recaptcha' not in data:
            raise ValidationError('Recaptcha data not sent.')
        ip, _ = get_client_ip(self.context['request'])
        response = requests.post(
            url=f'https://www.google.com/recaptcha/api/siteverify?'
                f'secret={settings.DRF_RECAPTCHA_SECRET_KEY}&response={data["recaptcha"]}&remoteip=127.0.0.1',
            json={
                'secret': settings.DRF_RECAPTCHA_SECRET_KEY,
                'response': data['recaptcha'],
                'remoteip': ip,
            }
        )
        if response.status_code != 200 or not response.json().get('success', False):
            raise ValidationError('Recaptcha validation failed')
        return super().to_internal_value(data)


class SlideSerializer(serializers.ModelSerializer):
    desktop_resized = serializers.SerializerMethodField()   
    desktop_webp = serializers.SerializerMethodField()
    mobile_webp = serializers.SerializerMethodField()

    def get_desktop_resized(self, obj):
            request = self.context.get("request")
            resize_w = request.query_params.get('resize_w',None)
            resize_h = request.query_params.get('resize_h',None)
            domain = Site.objects.get_current().domain
            if resize_h is None and resize_w is None:
                resize_w = "1440"
            if resize_w is None:
                resize_w = ""
            if resize_h is None:
                height = ""
            else:
                height = f"x{resize_h}"
            if obj.slide.desktop_image:
                return domain+get_thumbnail(obj.slide.desktop_image, f'{resize_w}{height}', quality=100, format="PNG").url

    def get_desktop_webp(self, obj):
            request = self.context.get("request")
            resize_w = request.query_params.get('resize_w',None)
            resize_h = request.query_params.get('resize_h',None)
            domain = Site.objects.get_current().domain
            if resize_h is None and resize_w is None:
                resize_w = "1440"
            if resize_w is None:
                resize_w = ""
            if resize_h is None:
                height = ""
            else:
                height = f"x{resize_h}"
            if obj.slide.desktop_image:
                return domain+get_thumbnail(obj.slide.desktop_image, f'{resize_w}{height}', quality=100, format="WEBP").url
    
    def get_mobile_webp(self, obj):
            # request = self.context.get("request")
            # resize_w = request.query_params.get('resize_w',None)
            # resize_h = request.query_params.get('resize_h',None)
            domain = Site.objects.get_current().domain
            # if resize_h is None and resize_w is None:
            #     resize_w = "600"
            # if resize_w is None:
            #     resize_w = ""
            # if resize_h is None:
            #     height = ""
            # else:
            #     height = f"x{resize_h}"
            if obj.slide.mobile_image:
                return domain+get_thumbnail(obj.slide.mobile_image,f"640", quality=100, format="WEBP").url
    class Meta:
        model = SliderSlidesThroughModel
        fields = '__all__'
        depth = 2


class SliderSerializer(serializers.ModelSerializer):
    # slides = serializers.SerializerMethodField()
    slider_slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Slider
        fields = '__all__'
        depth = 2


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'
        lookup_field = 'key'