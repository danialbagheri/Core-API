import ast

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from ipware import get_client_ip
from rest_framework import serializers

from user.models import VariantImageRequest
from user.tasks import SendVariantImagesEmailTask
from ..validators import SkuListValidator


class VariantImageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImageRequest
        fields = (
            'id',
            'sku_list',
            'image_type',
            'image_angle',
            'image_format',
            'email',
        )
        read_only_fields = (
            'id',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recaptcha_value = None

    def to_internal_value(self, data):
        self.recaptcha_value = data.get('recaptcha')
        if data.get('sku_list'):
            data['sku_list'] = str(data['sku_list'])
        return super().to_internal_value(data)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        sku_list = ast.literal_eval(attrs['sku_list'])
        SkuListValidator(sku_list).validate_sku_list()

        if '@lincocare.com' not in attrs['email']:
            raise ValidationError({'email': 'Email must be from the domain "lincocare.com"'})

        if not self.recaptcha_value:
            raise ValidationError('Recaptcha data not sent.')
        ip, _ = get_client_ip(self.context['request'])
        response = requests.post(
            url=f'https://www.google.com/recaptcha/api/siteverify?'
                f'secret={settings.DRF_RECAPTCHA_SECRET_KEY}&response={self.recaptcha_value}&remoteip={ip}',
        )
        data = response.json()
        if response.status_code != 200 or not data.get('success', False):
            raise ValidationError('Recaptcha validation failed.')
        return attrs

    def create(self, validated_data):
        variant_image_request = super().create(validated_data)
        SendVariantImagesEmailTask().delay(variant_image_request.id)
        return variant_image_request
