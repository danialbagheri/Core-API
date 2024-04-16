from django.conf import settings

from common.services import BaseService, TiktokClient


class OrderFulfillmentService(BaseService):
    service_name = 'Order Fulfillment Service'

    def __init__(self, order_data):
        super().__init__(order_data=order_data)
        self.order_data = order_data
        self.tiktok_client = TiktokClient()

    def _get_tiktok_order_id(self):
        note_attributes = self.order_data['note_attributes']
        for note_attribute in note_attributes:
            if note_attribute['name'] == 'TikTok Shop order number':
                return note_attribute['value']

    def _get_tracking_number(self):
        fulfillments = self.order_data['fulfillments']
        for fulfillment in fulfillments:
            tracking_number = fulfillment['tracking_number']
            if tracking_number:
                return tracking_number

    def fulfill_order(self):
        body = {
            'tiktok_order_id': self._get_tiktok_order_id(),
            'tracking_number': self._get_tracking_number(),
            'provider_id': settings.AMAZON_LOGISTICTS_PROVIDER_ID,
        }
        self.tiktok_client.send_post_request(
            path='/api/logistics/tracking',
            body=body,
        )
