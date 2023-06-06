from typing import Dict, Any, List

from bs4 import BeautifulSoup
from django.conf import settings

from common.services import TransactionalMailJetEmailService
from product.models import ProductVariant
from user.models import SentEmail
from web.models import Configuration


class InStockMailjetEmail(TransactionalMailJetEmailService):
    template_id = Configuration.objects.filter(key='in-stock-email-template-id').first()
    template_name = SentEmail.TEMPLATE_IN_STOCK

    def __init__(self, variant: ProductVariant, emails: List[str]):
        super().__init__(emails)
        self.variant = variant

    def _get_variables(self) -> Dict[str, Any]:
        variant_image = self.variant.variant_images.first()
        image_url = variant_image.image.url if variant_image else settings.LOST_PRODUCT_IMAGE_PATH
        image_url = f'{settings.WEBSITE_ADDRESS}{image_url}'
        plain_description = BeautifulSoup(self.variant.product.description).text
        return {
            'product_title': self.variant.product.name,
            'variant_title': self.variant.name,
            'variant_image': image_url,
            'shop_url': f'https://calypsosun.com/products/{self.variant.product.slug}',
            'product_description': f'{plain_description[:200]}...',
        }

    def _get_extra_data(self) -> str:
        return f'Variant ID: {self.variant.graphql_id}'
