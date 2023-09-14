from common.services import BaseService
from orders.models import AmazonOrder, AmazonOrderItem
from .amazon_review_reminder_creator import AmazonReviewReminderEditor


class AmazonOrderSyncer(BaseService):
    service_name = 'Order Syncer'

    def __init__(self, order_data):
        super().__init__(order_data=order_data)
        self.order_data = order_data['Payload']['OrderChangeNotification']

    def _sync_order_items(self, amazon_order):
        AmazonOrderItem.objects.filter(amazon_order=amazon_order).delete()
        amazon_order_items_to_create = []
        for order_item_data in self.order_data['Summary']['OrderItems']:
            amazon_order_items_to_create.append(AmazonOrderItem(
                amazon_order_item_id=order_item_data['OrderItemId'],
                amazon_order=amazon_order,
                sku=order_item_data['SellerSKU'],
                order_item_status=order_item_data.get('OrderItemStatus', ''),
                quantity=order_item_data['Quantity'],
                is_buyer_requested_cancel=order_item_data.get('IsBuyerRequestedCancel'),
            ))
        AmazonOrderItem.objects.bulk_create(amazon_order_items_to_create)

    def sync_order(self):
        summary = self.order_data['Summary']
        amazon_order, _ = AmazonOrder.objects.update_or_create(
            amazon_order_id=self.order_data['AmazonOrderId'],
            defaults={
                'seller_id': self.order_data['SellerId'],
                'order_status': summary['OrderStatus'],
                'fulfillment_type': summary['FulfillmentType'],
                'order_type': summary['OrderType'],
            }
        )
        self._sync_order_items(amazon_order)
        AmazonReviewReminderEditor(amazon_order).edit_review_reminder()
