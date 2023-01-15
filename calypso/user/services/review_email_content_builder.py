from typing import List

from django.conf import settings

from product.models import ProductVariant


class ReviewEmailContentBuilder:
    CONTENT_BASE = '''

'''

    def __init__(self, variants: List[ProductVariant]):
        self.variants = variants

    def _build_variant_content(self, variant):
        variant_image = variant.variant_images.first()
        image_url = variant_image.image.url if variant_image else '/media/email-images/lost-image.svg'
        image_url = f'{settings.WEBSITE_ADDRESS}{image_url}'
        product_name = f'{variant.product.name} {variant.name}'
        review_link = f'https://calypsosun.com/products/{variant.product.slug}/review'
        return self.CONTENT_BASE\
            .replace('{{image_url}}', image_url)\
            .replace('{{product_name}}', product_name)\
            .replace('{{review_link}}', review_link)

    def build_content(self):
        content = ''
        for variant in self.variants:
            variant_content = self._build_variant_content(variant)
            content += variant_content
        return content
