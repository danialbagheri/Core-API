from datetime import datetime, timedelta

from django.conf import settings
from sp_api.api import Orders

from common.services import BaseService


class AmazonOrderRetriever(BaseService):
    service_name = 'Amazon Order Retriever'

    def __init__(self, start_datetime=None, end_datetime=None):
        yesterday = datetime.now() - timedelta(days=1)
        self.start_datetime = start_datetime or yesterday
        self.end_datetime = end_datetime or (start_datetime + timedelta(days=1))
        super().__init__(start_datetime=self.start_datetime, end_datetime=self.end_datetime)
        self.orders_resource = Orders(credentials=settings.AMAZON_SP_API_CREDENTIALS)

    def _retrieve_orders(self, next_token=None):
        if next_token:
            return self.orders_resource.get_orders(NextToken=next_token)
        return self.orders_resource.get_orders(
            LastUpdatedAfter=self.start_datetime.strftime('%Y-%m-%d'),
            LastUpdatedBefore=self.end_datetime.strftime('%Y-%m-%d'),
            OrderStatuses=['Shipped', 'PartiallyShipped', 'InvoiceUnconfirmed'],
        )

    def retrieve_orders(self):
        orders = []
        next_token = None
        while True:
            response = self._retrieve_orders(next_token)
            orders += response.Orders
            next_token = response.next_token
            if next_token:
                break
        return orders
