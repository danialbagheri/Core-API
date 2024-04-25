from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from user.models import ProductInStockReport, ScheduledEmail
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
        if current_report:
            return current_report
        current_report = super().create(validated_data)
        ScheduledEmail.objects.get_or_create(
            recipient_email=current_report.email,
            template_name=ScheduledEmail.TEMPLATE_SUBSCRIBE_INVITATION,
            defaults={
                'send_time': timezone.now() + timedelta(weeks=2),
            },
        )
        return current_report
