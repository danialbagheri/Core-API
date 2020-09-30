from rest_framework import serializers
from drf_recaptcha.fields import ReCaptchaV2Field, ReCaptchaV3Field


class ContactFormSerializer(serializers.Serializer):
    choices = [
        'Product Question',
        'Urgent: Change Order detail or Address',
        'Wholesale, Discount, promo code query',
        'Question about order or Delivery',
        'Press Contact & Media',
        'Other'
    ]
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    reason = serializers.ChoiceField(choices=['red', 'green', 'blue'],)
    message = serializers.TextField()
    recaptcha = ReCaptchaV2Field()
