from typing import Dict, Any, List

from django.conf import settings

from common.services import TransactionalMailJetEmailService
from product.models import ProductVariant
from user.models import SentEmail
from web.models import Configuration


class ReviewReminderMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_REVIEW_REMINDER

    def __init__(self, variants: List[ProductVariant], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variants = variants

    def _get_template_id(self):
        template_id_config = Configuration.objects.filter(key='review-reminder-email-template-id').first()
        if not template_id_config:
            return None
        return int(template_id_config.value)

    def _get_variables(self) -> Dict[str, Any]:
        variants_data = []
        for variant in self.variants:
            variant_image = variant.variant_images.first()
            image_url = variant_image.image.url if variant_image else settings.LOST_PRODUCT_IMAGE_PATH
            image_url = f'{settings.BACKEND_ADDRESS}{image_url}'
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
