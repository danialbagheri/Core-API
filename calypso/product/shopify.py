import requests
from django.conf import settings

base_url = settings.SHOPIFY_URL
api_key = settings.SHOPIFY_API_KEY
password = settings.SHOPIFY_PASSWORD
graphql_url = "https://lincocare.myshopify.com/admin/api/2020-07/graphql.json"
#  shopify.ShopifyResource.set_site(base_url)
# shopify.Customer.search(query="bagheri.danial@gmail.com")


def get_variant_info_by_restVariantId(restVariantId):
    headers = {"X-Shopify-Access-Token": password}
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
    r = requests.post(url=graphql_url, json={'query': query}, headers=headers)
    return r.json()['data']['productVariant']


def get_variant_info_by_sku(sku):
    headers = {"X-Shopify-Access-Token": password}
    query = '''
{
  productVariants(first: 1, query: "sku:%s") {
    edges {
      node {
        price
        storefrontId
        displayName
        legacyResourceId
        inventoryQuantity
      }
    }
  }
}   
    ''' % sku
    r = requests.post(url=graphql_url, json={'query': query}, headers=headers)
    return r.json()['data']['productVariants']['edges'][0]['node']
