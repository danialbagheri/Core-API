from decimal import Decimal

from bundles.models import Bundle
from common.services import BaseService


class BundlePriceProcessor(BaseService):
    service_name = 'Bundle Price Processor'

    def __init__(self, bundle: Bundle):
        super().__init__(bundle=bundle)
        self.bundle = bundle
        self.compare_at_price = 0
        self.final_price = 0
        self.euro_compare_at_price = 0
        self.euro_final_price = 0

    def _calculate_compare_at_price(self):
        items = self.bundle.items.all()
        for item in items:
            variant = item.variants.first()
            if not variant:
                continue

            self.compare_at_price += (variant.compare_at_price or variant.price) * item.quantity
            self.euro_compare_at_price += (variant.euro_compare_at_price or variant.euro_price) * item.quantity

    def _calculate_final_price(self):
        self.final_price = Decimal(self.bundle.price) * (100 - self.bundle.discount_percentage) / 100
        self.final_price = float(self.final_price)

    def process_bundle_price(self):
        self._calculate_compare_at_price()
        self._calculate_final_price()
