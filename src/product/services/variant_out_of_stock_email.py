from django.conf import settings

from common.services import MarketingEmailService
from product.models import ProductVariant


class VariantOutOfStockEmailService(MarketingEmailService):
    subject = f'{settings.BRAND_NAME}: Variant Out of Stock'
    message = '''
Variant {variant_name} with SKU {variant_sku} is out of stock.
'''
    service_name = 'Variant Out of Stock Email Service'

    def __init__(self, variant: ProductVariant):
        super().__init__(variant=variant)
        self.variant = variant

    def get_variables(self):
        return {
            'variant_name': f'{self.variant.product.name} - {self.variant.name}',
            'variant_sku': self.variant.sku,
        }
