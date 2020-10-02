from rest_framework import serializers
from drf_recaptcha.fields import ReCaptchaV2Field, ReCaptchaV3Field


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
