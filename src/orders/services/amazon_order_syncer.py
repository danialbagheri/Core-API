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
        purchase_date = self.order_data.get('PurchaseDate')
        earliest_delivery_date = self.order_data.get('EarliestDeliveryDate')
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        amazon_order, _ = AmazonOrder.objects.update_or_create(
            amazon_order_id=self.order_data['AmazonOrderId'],
            defaults={
                'purchase_date': datetime.strptime(purchase_date, date_format) if purchase_date else None,
                'earliest_delivery_date':
                    datetime.strptime(earliest_delivery_date, date_format) if earliest_delivery_date else None,
                'order_status': self.order_data['OrderStatus'],
                'fulfillment_type': self.order_data['FulfillmentChannel'],
                'order_type': self.order_data['OrderType'],
            }
        )
        AmazonReviewReminderEditor(amazon_order).edit_review_reminder()
