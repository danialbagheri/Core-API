import logging

import requests
from django.conf import settings

from common.services import BaseService

logger = logging.getLogger(__name__)


class EmailOrderVerifier(BaseService):
    service_name = 'Email Order Verifier'
    EMAIL_ORDER_QUERY = '''
{
  orders(first:1 query:"email:%s") {
    nodes{
      id
    }
  }
}
'''

    def __init__(self, email: str):
        super().__init__(email=email)
        self.email = email

    def verify_email_order(self):
        query = self.EMAIL_ORDER_QUERY.format(self.email)
        response = requests.post(
            url=settings.SHOPIFY_URL,
            json={'query': query},
            headers={'X-Shopify-Access-Token': settings.SHOPIFY_PASSWORD},
        )
        data = response.json()
        if not response.ok or 'data' not in data:
            logger.exception('Failed to retrieve orders.')
            return True
        orders = data['data']['orders']['nodes']
        return bool(orders)
