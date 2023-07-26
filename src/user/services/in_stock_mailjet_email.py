from typing import Dict, Any, List

from bs4 import BeautifulSoup
from django.conf import settings

from common.services import TransactionalMailJetEmailService
from product.models import ProductVariant
from user.models import SentEmail
from web.models import Configuration


class InStockMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_IN_STOCK

    def __init__(self, variant: ProductVariant, emails: List[str]):
        super().__init__(emails)
        self.variant = variant

    def _get_template_id(self):
        template_id_config = Configuration.objects.filter(key='in-stock-email-template-id').first()
        if not template_id_config:
            return None
        return int(template_id_config.value)

    def _get_variables(self) -> Dict[str, Any]:
        variant_image = self.variant.variant_images.first()
        image_url = variant_image.image.url if variant_image else settings.LOST_PRODUCT_IMAGE_PATH
        if not settings.USE_S3:
            image_url = f'{settings.BACKEND_ADDRESS}{image_url}'
        plain_description = BeautifulSoup(self.variant.product.description, features='html.parser').text
        return {
            'product_title': self.variant.product.name,
            'variant_title': self.variant.name,
            'variant_image': image_url,
            'shop_url': f'{settings.WEBSITE_ADDRESS}/products/{self.variant.product.slug}?sku={self.variant.sku}',
            'product_description': f'{plain_description[:200]}...',
        }

    def _get_extra_data(self) -> str:
        return f'Variant ID: {self.variant.graphql_id}'
