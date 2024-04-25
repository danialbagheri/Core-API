from typing import List

from django.conf import settings

from common.services import TransactionalMailJetEmailService
from product.models import ProductVariant
from user.models import SentEmail
from web.models import Configuration


class SurveyResultsMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_SURVEY_RESULTS

    def __init__(self, variants: List[ProductVariant], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variants = variants

    def _get_template_id(self):
        template_id_config = Configuration.objects.filter(key='survey-results-email-template-id').first()
        if not template_id_config:
            return None
        return int(template_id_config.value)

    def _get_variables(self):
        variants_data = []
        for variant in self.variants:
            variant_image = variant.variant_images.filter(main=True).first()
            if not variant_image:
                variant_image = variant.variant_images.first()
            image_url = variant_image.image.url if variant_image else settings.LOST_PRODUCT_IMAGE_PATH
            variants_data.append({
                'variant_image': image_url,
                'variant_title': variant.name,
                'product_title': variant.product.name,
            })
        return {
            'white_logo_url': 'https://calypso-static.s3.eu-west-2.amazonaws.com/media/email-images/Calypso-white.png',
            'website_url': 'https://calypsosun.com',
            'secondary_text_color': 'white',
            'primary_background_color': '#ff6b00',
            'primary_text_color': '#ff6b00',
            'discount_code': 'P2HNMT42GKA1',
            'variants_data': variants_data
          }

    def _get_extra_data(self):
        sku_list = [variant.sku for variant in self.variants]
        return f'SKU List: {sku_list}'
