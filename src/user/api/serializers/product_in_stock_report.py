from rest_framework import serializers

from user.models import ProductInStockReport
from ..validators import ProductInStockReportValidator


class ProductInStockReportSerializer(serializers.ModelSerializer):
    variant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProductInStockReport
        fields = (
            'id',
            'variant_id',
            'email',
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
        current_report = self._report_validator.current_report
        if not current_report:
            current_report = super().create(validated_data)
        return current_report
