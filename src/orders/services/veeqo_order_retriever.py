from django.conf import settings

from common.services import BaseService, VeeqoClient

class VeeqoOrderRetriever(BaseService):
    service_name = 'Veeqo Order Retriever'

    def __init__(self, shopify_order_id):
        super().__init__(shopify_order_id=shopify_order_id)
        self.shopify_order_id = shopify_order_id
        self.veeqo_client = VeeqoClient()
        # every sales channel has different channel id on Veeqo
        # self.channel_id = settings.VEEQO_CHANNEL_ID # 62683 for Calypso Shopify

    def _query_orders(self):
        orders =self.veeqo_client.send_get_request(
            path=f'/orders?query={self.shopify_order_id}&channel_id=62683'
        )
        return orders

    def get_tracking_number(self) -> str:
        order = self._query_orders()[0]
        shipment =order['allocations']['shipment']
        return shipment['tracking_number']['tracking_number']