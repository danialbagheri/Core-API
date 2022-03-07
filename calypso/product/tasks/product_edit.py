import logging

import requests
from celery import Task
from django.conf import settings

from product.models import ProductVariant, Product

logger = logging.getLogger(__name__)

PRODUCT_RETRIEVE_QUERY = '''
{
  products(first: 1 query: "legacyResourceId:{product_id}") {
    edges {
      node {
        id
        variants(first: 10) {
          edges {
            node{
              id
              price
              compareAtPrice
              availableForSale
              barcode
              updatedAt
              displayName
              legacyResourceId
              inventoryQuantity
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
  }
}
'''


class ProductEditTask(Task):
    name = 'ProductEdit'

    @staticmethod
    def update_variants(product, variants_data):
        for variant_data in variants_data['edges']:
            data = variant_data['node']
            presentment_prices = data['presentmentPrices']['edges']
            euro_info = None
            if presentment_prices:
                euro_info = presentment_prices[0]['node']
            ProductVariant.objects.update_or_create(
                shopify_rest_variant_id=data['legacyResourceId'],
                defaults={
                    'sku': data['sku'],
                    'product': product,
                    'price': data['price'],
                    'compare_at_price': data['compareAtPrice'],
                    'inventory_quantity': data['inventory_quantity'],
                    'barcode': data['barcore'],
                    'euro_price': euro_info['price']['amount'] if euro_info else None,
                    'euro_compare_at_price':
                        euro_info['compareAtPrice']['amount'] if euro_info and euro_info['compareAtPrice'] else None
                }
            )

    def run(self, product_id):
        response = requests.post(
            url='https://lincocare.myshopify.com/admin/api/2020-07/graphql.json',
            json={
                'query': PRODUCT_RETRIEVE_QUERY.format(product_id=product_id),
            },
            headers={'X-Shopify-Access-Token': settings.SHOPIFY_PASSWORD}
        )
        if not response.ok:
            logger.warning(f'Failed to retrieve product {product_id}')
            return
        data = response.json()['data']['product']
        product, created = Product.objects.get_or_create(
            graphql_id=data['id'],
            defaults={
                'legacy_id': product_id,
            }
        )
        self.update_variants(product, data['variants'])
