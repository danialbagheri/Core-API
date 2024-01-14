from common.services import BaseService
from orders.models import AmazonOrder
from .amazon_review_reminder_creator import AmazonReviewReminderEditor


class AmazonOrderSyncer(BaseService):
    service_name = 'Order Syncer'

    def __init__(self, order_data):
        super().__init__(order_data=order_data)
        self.order_data = order_data['Payload']['OrderChangeNotification']

    def sync_order(self):
        summary = self.order_data['Summary']
        amazon_order, _ = AmazonOrder.objects.update_or_create(
            amazon_order_id=self.order_data['AmazonOrderId'],
            defaults={
                'seller_id': self.order_data['SellerId'],
                'order_status': summary['OrderStatus'],
                'fulfillment_type': summary['FulfillmentChannel'],
                'order_type': summary['OrderType'],
            }
        )
        AmazonReviewReminderEditor(amazon_order).edit_review_reminder()
