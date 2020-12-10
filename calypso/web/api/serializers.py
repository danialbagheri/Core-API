from rest_framework import serializers
from drf_recaptcha.fields import ReCaptchaV2Field, ReCaptchaV3Field
from web.models import Slider, Slide, SliderSlidesThroughModel, Configuration, Setting


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
    recaptcha = ReCaptchaV2Field()


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderSlidesThroughModel
        fields = ('slide', 'order')
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