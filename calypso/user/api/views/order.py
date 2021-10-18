import requests
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class OrderAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def _get_orders_query(self, cursor=None):
        email = self.request.user.email
        cursor_filter = f'after: "{cursor}"' if cursor else ''
        return '''
{
  orders(
    first: 10
    query: "email:%s"
    sortKey: CREATED_AT
    reverse: true
    %s
  ) {
    edges {
      node {
        createdAt
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        lineItems(first:10) {
          edges {
            node {
              image {
                id
                originalSrc
                transformedSrc
              }
              name
              title
              quantity
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

        ''' % (email, cursor_filter)

    @staticmethod
    def _get_response_data(response):
        data = {'orders': []}
        orders_list = response['edges']
        data['has_next_page'] = response['pageInfo']['hasNextPage']
        data['cursor'] = orders_list[-1]['cursor'] if orders_list else None
        for order in orders_list:
            order_node = order['node']
            order_data = {
                'created_at': order_node['createdAt'],
                'price': order_node['totalPriceSet']['shopMoney']['amount'],
                'currency': order_node['totalPriceSet']['shopMoney']['currencyCode'],
            }
            response_items = order_node['lineItems']['edges']
            items_data = []
            for item in response_items:
                item_node = item['node']
                image = item_node['image']
                item_data = {
                    'image_original_source': image['originalSrc'] if image else None,
                    'image_transformed_source': image['transformedSrc'] if image else None,
                    'name': item_node['name'],
                    'title': item_node['title'],
                    'quantity': item_node['quantity'],
                }
                items_data.append(item_data)
            order_data['items'] = items_data
            data['orders'].append(order_data)
        return data

    def get(self, *args, **kwargs):
        cursor = None
        results = []
        while True:
            query = self._get_orders_query(cursor)
            response = requests.post(
                url='https://lincocare.myshopify.com/admin/api/2020-07/graphql.json',
                json={
                    'query': query,
                },
                headers={"X-Shopify-Access-Token": settings.SHOPIFY_PASSWORD}
            )
            if response.status_code < 200 or response.status_code >= 300:
                return Response(
                    data=response.text,
                    status=response.status_code,
                )
            response_data = self._get_response_data(response.json()['data']['orders'])
            results += response_data['orders']
            if not response_data['has_next_page']:
                break
            cursor = response_data['cursor']
        return Response(
            data=results,
            status=status.HTTP_200_OK,
        )
