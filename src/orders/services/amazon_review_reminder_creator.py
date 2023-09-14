from datetime import timedelta

from django.db import transaction

from common.services import BaseService
from orders.models import AmazonOrder
from product.models import ProductVariant
from user.models import AmazonReviewReminder, AmazonReviewReminderBoughtVariant


class AmazonReviewReminderEditor(BaseService):
    service_name = 'Amazon Review Reminder Creator'

    def __init__(self, amazon_order: AmazonOrder):
        super().__init__(amazon_order_id=amazon_order.id)
        self.amazon_order = amazon_order

    def _delete_review_reminder(self):
        AmazonReviewReminder.objects.filter(amazon_order=self.amazon_order).delete()

    def _edit_order_bought_variants(self, review_reminder):
        AmazonReviewReminderBoughtVariant.objects.filter(review_reminder=review_reminder).delete()
        items = self.amazon_order.items.all()
        variants_map = {variant.sku: variant.id for variant in ProductVariant.objects.all()}
        review_reminder_bought_variants = []

        for item in items:
            sku = item.sku
            variant_id = variants_map.get(sku)
            if not variant_id or not item.quantity:
                continue
            review_reminder_bought_variants.append(AmazonReviewReminderBoughtVariant(
                review_reminder=review_reminder,
                variant_id=variant_id,
                quantity=item.quantity,
            ))
        AmazonReviewReminderBoughtVariant.objects.bulk_create(review_reminder_bought_variants)

    def edit_review_reminder(self):
        if self.amazon_order.ORDER_STATUS_CANCELED:
            self._delete_review_reminder()
            return

        reminder_date = self.amazon_order.purchase_date + timedelta(days=21)

        with transaction.atomic():
            review_reminder, _ = AmazonReviewReminder.objects.get_or_create(
                amazon_order=self.amazon_order,
                defaults={
                    'reminder_date': reminder_date,
                },
            )
            self._edit_order_bought_variants(review_reminder)
