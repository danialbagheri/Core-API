from typing import Dict, Any

from django.conf import settings

from common.services import TransactionalMailJetEmailService
from product.services import RelatedProductsRetriever
from review.models import Review
from user.models import SentEmail
from web.models import Configuration


class ReviewApprovalMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_REVIEW_APPROVAL

    def __init__(self, review: Review, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.review = review
        self.related_products = RelatedProductsRetriever(review.product).get_related_products(3)

    def _get_template_id(self):
        template_id_config = Configuration.objects.filter(key='review-approval-email-template-id').first()
        if not template_id_config:
            return None
        return int(template_id_config.value)

    def _get_variables(self) -> Dict[str, Any]:
        product = self.review.product
        variant = self.review.variant
        variant_image = variant.variant_images.first() if variant else None
        image_url = variant_image.image.url if variant_image else settings.LOST_PRODUCT_IMAGE_PATH
        image_url = f'{settings.BACKEND_ADDRESS}{image_url}'
        variables = {
            'variant_image': image_url,
            'product_title': product.name,
            'variant_title': variant.name,
            'review_url': f'{settings.WEBSITE_ADDRESS}/products/{product.slug}#readReviews',
        }
        for index, related_product in enumerate(self.related_products):
            number = index + 1
            variant = related_product.variants.filter(is_public=True).first()
            variant_image = variant.variant_images.first() if variant else None
            image_url = variant_image.image.url if variant_image else settings.LOST_PRODUCT_IMAGE_PATH
            image_url = f'{settings.BACKEND_ADDRESS}{image_url}'
            variables.update({
                f'recommended_variant_image_{number}': image_url,
                f'recommended_product_title_{number}': related_product.name,
                f'recommended_product_subtitle_{number}': related_product.sub_title,
                f'recommended_product_url_{number}': f'{settings.WEBSITE_ADDRESS}/products/{related_product.slug}',
            })
        return variables

    def _get_extra_data(self) -> str:
        return f'Review ID: {self.review.id}'
