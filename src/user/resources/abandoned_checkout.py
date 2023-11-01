import requests
from django.conf import settings


class AbandonedCheckoutResource:
    def __init__(self):
        self.url = f'https://{settings.SHOPIFY_DOMAIN}/admin/api/{settings.SHOPIFY_API_VERSION}/checkouts.json'
        self.headers = {'X-Shopify-Access-Token': settings.SHOPIFY_PASSWORD}
        self.next_page_url = None

    def get_abandoned_checkouts(self, url=None, **params):
        if url:
            response = requests.get(url, headers=self.headers)
        else:
            response = requests.get(self.url, params=params, headers=self.headers)
        checkouts = response.json()['checkouts']
        link_header = response.headers.get('Link')
        if link_header:
            self.next_page_url = link_header[1: link_header.index('>')]
        return checkouts
