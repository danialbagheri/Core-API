from django.core.exceptions import ValidationError
from rest_framework import serializers

from common.services import RecaptchaValidator
from user.models import VariantImageRequest
from user.tasks import SendVariantImagesEmailTask
from ..validators import ImageRequestFiltersValidator


class VariantImageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImageRequest
        fields = (
            'id',
            'sku_list',
            'image_types',
            'image_angles',
            'image_formats',
            'no_directories',
            'email',
        )
        read_only_fields = (
            'id',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recaptcha_value = None
        self.invalid_sku_list = []

    def to_internal_value(self, data):
        self.recaptcha_value = data.get('recaptcha')
        list_filters = ['sku_list', 'image_types', 'image_angles', 'image_formats']

        for list_filter in list_filters:
            if list_filter in data:
                data[list_filter] = str(data[list_filter])

        for list_filter in list_filters[1:]:
            if list_filter not in data and list_filter[:-1] in data:
                data[list_filter] = str([data.pop(list_filter[:-1])])
        return super().to_internal_value(data)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        validator = ImageRequestFiltersValidator(attrs)
        validator.validate()
        self.invalid_sku_list = validator.invalid_sku_list
        attrs['sku_list'] = validator.sku_list

        if not validator.sku_list:
            raise ValidationError('No valid sku.')

        if not self.recaptcha_value:
            raise ValidationError('Recaptcha data not sent.')
        RecaptchaValidator(self.recaptcha_value).validate(self.context['request'])
        return attrs

    def create(self, validated_data):
        variant_image_request = super().create(validated_data)
        SendVariantImagesEmailTask().delay(variant_image_request.id)
        return variant_image_request

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'invalid_sku_list': self.invalid_sku_list,
            'image_request': representation,
        }
