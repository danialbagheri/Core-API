import urllib
from typing import Any, Dict

from django.conf import settings

from common.services import TransactionalMailJetEmailService
from product.models import ProductType
from user.models import SentEmail


class CategoriesIntroEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_CATEGORIES_INTRO
    template_config_key = 'categories-intro-template-id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_types = ProductType.objects.all().order_by('id')

    def _get_variables(self) -> Dict[str, Any]:
        variables = []
        for product_type in self.product_types:
            image = product_type.image
            image_url = image.url if image else settings.LOST_PRODUCT_IMAGE_PATH
            params = {'category': product_type.name}
            variables.append({
                'category_name': product_type.name,
                'category_image_url': image_url,
                'category_page_url': f'{settings.WEBSITE_ADDRESS}/products?{urllib.parse.urlencode(params)}'
            })
        return {'categories': variables}

    def _get_extra_data(self) -> str:
        return ''
