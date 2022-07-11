from datetime import timedelta

from django.utils import timezone

from product.models import ProductVariant
from user.models import ReviewReminder


class ReviewReminderCreatorService:

    @staticmethod
    def _get_variant_ids(line_items):
        variants_map = {variant.shopify_rest_variant_id: variant.id for variant in ProductVariant.objects.all()}
        variant_ids = []

        for line_item in line_items:
            shopify_variant_id = line_item['variant_id']
            variant_id = variants_map[shopify_variant_id]
            variant_ids.append(variant_id)
        return variant_ids

    @classmethod
    def create_review_reminder(cls, order_data):
        order_id = order_data['id']
        email = order_data['email']
        variant_ids = cls._get_variant_ids(order_data['line_items'])
        reminder_date = timezone.now() + timedelta(days=21)

        review_reminder = ReviewReminder.objects.create(
            order_id=order_id,
            email=email,
            reminder_date=reminder_date,
        )
        review_reminder.bought_variants.add(*variant_ids)
