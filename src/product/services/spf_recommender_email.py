from typing import List, Dict, Any

from django.conf import settings

from common.services import TransactionalMailJetEmailService
from product.models import ProductVariant
from user.models import SentEmail


class SPFRecommenderMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_SPF_RECOMMENDER
    template_config_key = 'spf-recommender-template-id'

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
                'variant_image': image_url,
                'review_average_score': variant.product.get_review_average_score,
                'price': '%.2f' % variant.price,
                'compare_at_price': '%.2f' % variant.compare_at_price if variant.compare_at_price else '',
            })
        return {
            'variants_data': variants_data,
        }

    def _get_extra_data(self) -> str:
        return ', '.join([variant.sku for variant in self.variants])

