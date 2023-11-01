from typing import Any, Dict

from django.conf import settings

from common.services import TransactionalMailJetEmailService
from user.models import AbandonedCheckout


class AbandonedCheckoutEmail(TransactionalMailJetEmailService):
    def __init__(self, checkout: AbandonedCheckout, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checkout = checkout

    def _get_variables(self) -> Dict[str, Any]:
        checkout_items_data = []
        items = self.checkout.items.select_related('variant', 'variant__product').all()
        for item in items:
            variant = item.variant
            variant_image = variant.variant_images.first()
            image_url = variant_image.image.url if variant_image else settings.LOST_PRODUCT_IMAGE_PATH
            checkout_items_data.append({
                'product_title': variant.product.title,
                'variant_title': variant.title,
                'variant_image': image_url,
            })
        return {
            'checkout_items': checkout_items_data,
            'checkout_url': self.checkout.abandoned_checkout_url,
        }

    def _get_extra_data(self) -> str:
        return f'Checkout ID: {self.checkout.legacy_id}, Customer ID: {self.checkout.customer_id}'
