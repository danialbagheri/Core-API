from datetime import datetime, timedelta

from django.conf import settings
from sp_api.api import Orders

from common.services import BaseService


class AmazonOrderRetriever(BaseService):
    service_name = 'Amazon Order Retriever'

    def __init__(self, start_datetime=None, end_datetime=None):
        yesterday = datetime.now() - timedelta(days=1)
        self.start_datetime = start_datetime or yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        self.end_datetime = end_datetime or (start_datetime + timedelta(days=1))
        super().__init__(start_datetime=self.start_datetime, end_datetime=self.end_datetime)

    def retrieve_orders(self):
        orders = Orders().get_orders(
            MarketplaceIds=[settings.AMAZON_MARKETPLACE_ID],
            LastUpdatedAfter=self.start_datetime,
            LastUpdatedBefore=self.end_datetime,
            OrderStatuses=['Shipped', 'PartiallyShipped', 'InvoiceUnconfirmed'],
        )
        return orders.payload['Orders']
