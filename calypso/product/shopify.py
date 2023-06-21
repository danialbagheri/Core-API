import requests
from django.conf import settings

#  shopify.ShopifyResource.set_site(base_url)
# shopify.Customer.search(query="bagheri.danial@gmail.com")


def get_variant_info_by_restVariantId(restVariantId):
    headers = {"X-Shopify-Access-Token": settings.SHOPIFY_PASSWORD}
    query = '''
{
    productVariant (id: "gid://shopify/ProductVariant/%s") {
         price
         sku
         displayName
         storefrontId
    }
}
    ''' % restVariantId
    r = requests.post(url=settings.SHOPIFY_URL, json={'query': query}, headers=headers)
    return r.json()['data']['productVariant']


def get_variant_info_by_sku(sku):
    headers = {"X-Shopify-Access-Token": settings.SHOPIFY_PASSWORD}
    query = '''
{
  productVariants(first: 1, query: "sku:%s") {
    edges {
      node {
        price
        compareAtPrice
        availableForSale
        barcode
        updatedAt
        storefrontId
        displayName
        legacyResourceId
        inventoryQuantity
        position
        presentmentPrices(first:1, presentmentCurrencies:[EUR]) {
          edges {
            node {
              price {
                amount
              }
              compareAtPrice {
                amount
              }
            }
          }
        }
      }
    }
  }
}   
    ''' % sku
    r = requests.post(url=settings.SHOPIFY_URL, json={'query': query}, headers=headers)
    return r.json()['data']['productVariants']['edges'][0]['node']
