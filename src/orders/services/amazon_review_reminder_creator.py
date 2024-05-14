from datetime import timedelta

from django.db import transaction

from common.services import BaseService
from orders.models import AmazonOrder
from user.models import AmazonReviewReminder


class AmazonReviewReminderEditor(BaseService):
    service_name = 'Amazon Review Reminder Creator'

    def __init__(self, amazon_order: AmazonOrder):
        super().__init__(amazon_order_id=amazon_order.id)
        self.amazon_order = amazon_order

    def _delete_review_reminder(self):
        AmazonReviewReminder.objects.filter(amazon_order=self.amazon_order).delete()

    def edit_review_reminder(self):
        if self.amazon_order.order_status == AmazonOrder.ORDER_STATUS_CANCELED:
            self._delete_review_reminder()
            return

        base_date = self.amazon_order.earliest_delivery_date or self.amazon_order.purchase_date
        reminder_date = base_date + timedelta(days=21)
        with transaction.atomic():
            review_reminder, _ = AmazonReviewReminder.objects.get_or_create(
                amazon_order=self.amazon_order,
                defaults={
                    'reminder_date': reminder_date,
                },
            )
