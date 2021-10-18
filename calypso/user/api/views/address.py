import requests
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class AddressAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def _get_addresses_query(self, cursor=None):
        email = self.request.user.email
        cursor_filter = f'after: "{cursor}"' if cursor else ''
        return '''
{
  customers(
    first: 10
    query: "email:%s"
    %s
  ) {
    edges {
      node {
        addresses(first: 10) {
          formatted
        }
      }
    }
  }
}
        ''' % (email, cursor_filter)

    @staticmethod
    def _get_response_data(response):
        data = {'addresses': []}
        customers_list = response['edges']
        data['has_next_page'] = response['pageInfo']['hasNextPage']
        data['cursor'] = customers_list[-1]['cursor'] if customers_list else None
        for customer in customers_list:
            customer_node = customer['node']
            addresses = customer_node['addresses']
            for address in addresses:
                data['addresses'].append({'address': address['formatted']})
        return data

    def get(self, *args, **kwargs):
        cursor = None
        results = []
        while True:
            query = self._get_addresses_query(cursor)
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
            response_data = self._get_response_data(response.json()['data']['customers'])
            results += response_data['addresses']
            if not response_data['has_next_page']:
                break
            cursor = response_data['cursor']
        return Response(
            data=results,
            status=status.HTTP_200_OK,
        )
