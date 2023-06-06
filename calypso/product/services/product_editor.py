import logging

import requests
from django.conf import settings

from product.models import Product, ProductVariant
from .product_in_stock_report_sender import ProductInStockReportSender

logger = logging.getLogger(__name__)

PRODUCT_RETRIEVE_QUERY = '''
{
  product(id: "%s") {
    id
    legacyResourceId
    handle
    title
    description
    variants(first: 10) {
      edges {
        node{
          id
          sku
          price
          compareAtPrice
          availableForSale
          barcode
          updatedAt
          displayName
          legacyResourceId
          inventoryQuantity
          position
          presentmentPrices(first:1, presentmentCurrencies:[EUR]) {
            edges {
              node {
                compareAtPrice {
                  amount
                }
                price {
                  amount
                }
              }
            }
          }
        }
        cursor
      }
      pageInfo {
        hasNextPage
      }
    }
  }
}
'''


class ProductEditor:
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.product = None
        self.in_stock_variants = []

    def _retrieve_product_data(self):
        logger.info(f'Retrieving {self.product_id}')
        response = requests.post(
            url='https://lincocare.myshopify.com/admin/api/2023-04/graphql.json',
            json={
                'query': PRODUCT_RETRIEVE_QUERY % self.product_id,
            },
            headers={'X-Shopify-Access-Token': settings.SHOPIFY_PASSWORD}
        )
        if not response.ok:
            logger.warning(f'Failed to retrieve product {self.product_id}')
            return
        return response.json()['data']['product']

    def _update_product(self, product_data):
        product, _ = Product.objects.get_or_create(
            graphql_id=self.product_id,
            defaults={
                'legacy_id': product_data['legacyResourceId'],
                'slug': product_data['handle'],
                'name': product_data['title'],
                'description': product_data['description'],
            }
        )
        self.product = product

    def _update_variants(self, variants_data):
        for variant_data in variants_data['edges']:
            data = variant_data['node']
            presentment_prices = data['presentmentPrices']['edges']
            euro_info = None
            if presentment_prices:
                euro_info = presentment_prices[0]['node']
            variant, _ = ProductVariant.objects.update_or_create(
                sku=data['sku'],
                defaults={
                    'sku': data['sku'],
                    'shopify_rest_variant_id': data['legacyResourceId'],
                    'graphql_id': data['id'],
                    'product': self.product,
                    'price': data['price'],
                    'compare_at_price': data['compareAtPrice'],
                    'inventory_quantity': data['inventoryQuantity'],
                    'barcode': data['barcode'],
                    'euro_price': euro_info['price']['amount'] if euro_info else None,
                    'euro_compare_at_price':
                        euro_info['compareAtPrice']['amount'] if euro_info and euro_info['compareAtPrice'] else None,
                    'position': data['position'],
                }
            )
            if variant.inventory_quantity > 0:
                self.in_stock_variants.append(variant)

    def edit_product(self):
        product_data = self._retrieve_product_data()
        self._update_product(product_data)
        self._update_variants(product_data['variants'])
        report_sender = ProductInStockReportSender(self.in_stock_variants)
        report_sender.send_in_stock_reports()
