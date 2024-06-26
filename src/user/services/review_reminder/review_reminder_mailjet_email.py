from typing import Dict, Any, List

from django.conf import settings

from common.services import TransactionalMailJetEmailService
from product.models import ProductVariant
from user.models import SentEmail


class ReviewReminderMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_REVIEW_REMINDER
    template_config_key = 'review-reminder-email-template-id'

    def __init__(self, variants: List[ProductVariant], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variants = variants

    def _get_variables(self) -> Dict[str, Any]:
        variants_data = []
        for variant in self.variants:
            variant_image = variant.variant_images.first()
            image_url = variant_image.image.url if variant_image else settings.LOST_PRODUCT_IMAGE_PATH
            variants_data.append({
                'product_title': variant.product.name,
                'variant_title': variant.name,
                'review_url': f'{settings.WEBSITE_ADDRESS}/products/write-review?slug={variant.product.slug}',
                'variant_image': image_url,
            })
        return {
            'variants_data': variants_data,
        }

    def _get_extra_data(self) -> str:
        email = self.emails[0]
        variant_ids = [variant.id for variant in self.variants]
        return f'Email: {email}, Variant Ids: {variant_ids}'
