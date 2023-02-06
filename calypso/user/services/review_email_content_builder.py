from typing import List

from django.conf import settings

from product.models import ProductVariant


class ReviewEmailContentBuilder:
    CONTENT_BASE = '''
<div style="width: 100%;margin-top: 80px;">
                 <div style="display: flex ">
                     <div style="background-image: url('{{image_url}}');background-position: center;background-size: contain;background-repeat: no-repeat;height:120px;min-height:120px; width:120px;min-width: 120px;margin-right:12px"></div>
                     <div>
                         <div style="font-size: 16px;font-weight: 400;line-height:25px;color: #3C1510;display: -webkit-box;-webkit-line-clamp: 3;-webkit-box-orient: vertical;overflow: hidden;">{{product_name}}</div>
                     </div>
                 </div>
                 <a href="{{review_link}}" style="text-decoration: none" target="_blank">
                     <div style="position: relative;width: 48%;cursor: pointer; margin-top: 20px;text-align: left; border: none;cursor: pointer;background-color: #FB4C1E;color: white;font-size: 14px;font-weight: 600;padding: 12px 16px;border-radius: 50px; ">
                         WRITE A REVIEW
                     </div>
                 </a>
            </div>
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
