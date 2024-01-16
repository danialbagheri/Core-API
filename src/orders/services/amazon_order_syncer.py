from datetime import datetime

from common.services import BaseService
from orders.models import AmazonOrder
from .amazon_review_reminder_creator import AmazonReviewReminderEditor


class AmazonOrderSyncer(BaseService):
    service_name = 'Order Syncer'

    def __init__(self, order_data):
        super().__init__(order_data=order_data)
        self.order_data = order_data

    def sync_order(self):
        amazon_order, _ = AmazonOrder.objects.update_or_create(
            amazon_order_id=self.order_data['AmazonOrderId'],
            defaults={
                'purchase_date': datetime.strptime(self.order_data['PurchaseDate'], '%Y-%m-%dT%H:%M:%S%Z'),
                'order_status': self.order_data['OrderStatus'],
                'fulfillment_type': self.order_data['FulfillmentChannel'],
                'order_type': self.order_data['OrderType'],
            }
        )
        AmazonReviewReminderEditor(amazon_order).edit_review_reminder()
