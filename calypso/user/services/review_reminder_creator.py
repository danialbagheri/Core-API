from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from product.models import ProductVariant
from user.models import ReviewReminder, ReviewReminderBoughtVariant


class ReviewReminderCreatorService:
    def __init__(self, order_data):
        self._order_data = order_data

    def _create_order_bought_variants(self, review_reminder):
        line_items = self._order_data['line_items']
        variants_map = {variant.shopify_rest_variant_id: variant.id for variant in ProductVariant.objects.all()}
        review_reminder_bought_variants = []

        for line_item in line_items:
            shopify_variant_id = line_item['variant_id']
            variant_id = variants_map.get(shopify_variant_id)
            if not variant_id:
                continue
            review_reminder_bought_variants.append(ReviewReminderBoughtVariant(
                review_reminder=review_reminder,
                variant_id=variant_id,
                quantity=line_item['quantity'],
            ))
        ReviewReminderBoughtVariant.objects.bulk_create(review_reminder_bought_variants)

    def create_review_reminder(self):
        order_id = self._order_data['id']
        email = self._order_data['email']
        reminder_date = timezone.now() + timedelta(days=21)

        with transaction.atomic():
            review_reminder = ReviewReminder.objects.create(
                order_id=order_id,
                email=email,
                reminder_date=reminder_date,
            )
            self._create_order_bought_variants(review_reminder)
