from rest_framework import serializers

from user.models import ProductInStockReport
from user.services import MarketingSubscriberService
from ..validators import ProductInStockReportValidator


class ProductInStockReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInStockReport
        fields = (
            'id',
            'variant_id',
            'email',
            'subscribe',
        )
        read_only_fields = (
            'id',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._report_validator = ProductInStockReportValidator()

    def validate(self, attrs):
        variant_id = attrs['variant_id']
        email = attrs['email']
        self._report_validator.is_valid(variant_id, email)
        return attrs

    def create(self, validated_data):
        subscribe_email = validated_data.pop('subscribe', None)
        if subscribe_email:
            email = validated_data['email']
            MarketingSubscriberService().subscribe_email(email)
        current_report = self._report_validator.current_report
        if not current_report:
            current_report = super().create(validated_data)
        return current_report
