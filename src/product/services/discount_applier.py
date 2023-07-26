from collections import defaultdict

import requests
from django.conf import settings


class DiscountApplierService:
    MUTATION_QUERY = '''
mutation productVariantsBulkUpdate(
  $productId: ID!,
  $variants: [ProductVariantsBulkInput!]!
) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants{
      id
      price
      compareAtPrice
    }
  }
}
'''

    def __init__(self, variants, discount_percentage):
        self.variants = variants
        self.discount_percentage = discount_percentage
        self.product_variants = defaultdict(list)
        self.variants_failed_to_alter = []

    def _map_product_variants(self):
        for variant in self.variants:
            self.product_variants[variant.product].append(variant)

    def _get_variants_data(self, variants):
        variants_data = []
        for variant in variants:
            compare_at_price = variant.compare_at_price or variant.price
            price = round(compare_at_price * (100 - self.discount_percentage) / 100, 2)
            if self.discount_percentage == 0:
                compare_at_price = None
            variant_data = {
                'id': variant.graphql_id,
                'price': price,
                'compareAtPrice': compare_at_price,
            }
            variants_data.append(variant_data)
        return variants_data

    def apply_discounts(self):
        self._map_product_variants()
        for product, variants in self.product_variants.items():
            variants_data = self._get_variants_data(variants)
            query_variables = {
                'productId': product.graphql_id,
                'variants': variants_data,
            }
            request_data = {
                'query': self.MUTATION_QUERY,
                'variables': query_variables,
            }
            response = requests.post(
                url=settings.SHOPIFY_URL,
                json=request_data,
                headers={'X-Shopify-Access-Token': settings.SHOPIFY_PASSWORD},
            )
            if not response.ok or 'data' not in response.json():
                self.variants_failed_to_alter += variants
