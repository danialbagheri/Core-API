from django.conf import settings
from django.db import transaction

from common.services import BaseService
from product.models import ProductVariant, WhereToBuy, Stockist


class AmazonLinkGenerator(BaseService):
    STOCKIST_NAME = 'Amazon UK'

    service_name = 'Amazon Link Generator'

    def __init__(self, variant: ProductVariant):
        super().__init__(variant=variant)
        self.variant = variant

    def _create_link_slug(self):
        product = self.variant.product
        product_slug = product.slug
        product_slug_length = len(product_slug.split('-'))
        if product_slug_length >= 5:
            return product_slug
        elif product_slug_length == 4:
            return f'{settings.BRAND_NAME}-{product_slug}'
        elif product_slug_length == 3:
            return f'{settings.BRAND_NAME}-{product_slug}-{self.variant.sku}'
        elif product_slug_length == 2:
            return f'{settings.BRAND_NAME}-{product_slug}-{self.variant.sku}-product'
        elif product_slug_length == 1:
            return f'{settings.BRAND_NAME}-{product_slug}-{self.variant.sku}-variant-product'

    def generate_amazon_link(self) -> None:
        link_slug = self._create_link_slug()
        if not self.variant.ASIN or not link_slug:
            return

        stockist = Stockist.objects.get_or_create(name=self.STOCKIST_NAME)
        with transaction.atomic():
            where_to_buy = WhereToBuy.objects.filter(
                variant=self.variant,
                stockist=stockist,
            ).first()
            if where_to_buy and (self.variant.ASIN not in where_to_buy.url):
                where_to_buy.delete()
            elif where_to_buy and (self.variant.ASIN in where_to_buy.url):
                return
            WhereToBuy.objects.create(
                variant=self.variant,
                stockist=stockist,
                url=f'https://www.amazon.co.uk/{link_slug}/dp/{self.variant.ASIN}'
            )
