import logging

import requests
from celery import Task
from django.conf import settings

from product.models import ProductVariant

logger = logging.getLogger(__name__)

VARIANTS_LIST_QUERY = '''
{
  productVariants(first: 100) {
    edges {
      node {
        product {
          id
          legacyResourceId
        }
        id
        legacyResourceId
      }
    }
  }
}
'''


class UpdateAllProductsTask(Task):
    name = 'UpdateAllProducts'

    def run(self):
        from product.tasks import ProductEditTask
        response = requests.post(
            url='https://lincocare.myshopify.com/admin/api/2020-07/graphql.json',
            json={
                'query': VARIANTS_LIST_QUERY,
            },
            headers={'X-Shopify-Access-Token': settings.SHOPIFY_PASSWORD}
        )
        if not response.ok:
            logger.warning(f'Failed to retrieve list of variants')
            return

        variants_data = response.json()['data']['productVariants']['edges']
        for variant_data in variants_data:
            data = variant_data['node']
            variant = ProductVariant.objects.filter(shopify_rest_variant_id=data['legacyResourceId']).first()
            if not variant:
                ProductEditTask().run(data['product']['id'])
                continue
            variant.graphql_id = data['id']
            variant.save()
            product = variant.product
            product.legacy_id = data['product']['legacyResourceId']
            product.graphql_id = data['product']['id']
            product.save()
