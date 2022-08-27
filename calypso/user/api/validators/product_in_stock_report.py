from rest_framework.exceptions import ValidationError

from product.models import ProductVariant
from user.models import ProductInStockReport


class ProductInStockReportValidator:
    def __init__(self):
        self.current_report = None

    def is_valid(self, variant_id: int, email: str):
        self.current_report = ProductInStockReport.objects.filter(
            variant_id=variant_id,
            email=email,
            email_sent=False,
        ).first()
        if self.current_report:
            return True

        variant = ProductVariant.objects.filter(id=variant_id).first()
        if not variant:
            raise ValidationError('Invalid variant id')
        if variant.inventory_quantity > 0:
            raise ValidationError('Variant is not out of stock')
        return True
