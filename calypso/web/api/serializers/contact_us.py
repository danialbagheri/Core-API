import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from ipware import get_client_ip
from rest_framework import serializers

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recaptcha_value = None

    def to_internal_value(self, data):
        self.recaptcha_value = data.get('recaptcha')
        return super().to_internal_value(data)

    def validate(self, attrs):
        if not self.recaptcha_value:
            raise ValidationError('Recaptcha data not sent.')

        ip, _ = get_client_ip(self.context['request'])
        response = requests.post(
            url=f'https://www.google.com/recaptcha/api/siteverify?'
                f'secret={settings.DRF_RECAPTCHA_SECRET_KEY}&response={self.recaptcha_value}&remoteip={ip}',
        )
        if response.status_code != 200 or not response.json().get('success', False):
            raise ValidationError('Recaptcha validation failed.')
        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def create(self, validated_data):
        return super().create(validated_data)
