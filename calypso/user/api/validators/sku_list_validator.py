from django.core.exceptions import ValidationError

from product.models import ProductVariant


class SkuListValidator:
    def __init__(self, sku_list):
        self.sku_list = [sku.upper() for sku in sku_list]

    def validate_sku_list(self):
        existing_sku_set = set(ProductVariant.objects.filter(sku__in=self.sku_list).values_list('sku', flat=True))
        invalid_sku_set = set(self.sku_list) - existing_sku_set
        if invalid_sku_set:
            raise ValidationError({'invalid_sku_list': list(invalid_sku_set)})
