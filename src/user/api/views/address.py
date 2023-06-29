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
        addresses {
          address1
          address2
          city
          company
          country
          countryCodeV2
          firstName
          id
          lastName
          phone
          province
          provinceCode
          zip
          formatted
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
        data = {'addresses': []}
        addresses_set = set()
        customers_list = response['edges']
        data['has_next_page'] = response['pageInfo']['hasNextPage']
        data['cursor'] = customers_list[-1]['cursor'] if customers_list else None
        for customer in customers_list:
            customer_node = customer['node']
            addresses = customer_node['addresses']
            for address in addresses:
                formatted = address['formatted']
                if str(formatted).lower() in addresses_set:
                    continue
                data['addresses'].append({
                    'id': address['id'],
                    'address1': address['address1'],
                    'address2': address['address2'],
                    'city': address['city'],
                    'company': address['company'],
                    'country': address['country'],
                    'country_code': address['countryCodeV2'],
                    'first_name': address['firstName'],
                    'last_name': address['lastName'],
                    'phone': address['phone'],
                    'province': address['province'],
                    'province_code': address['provinceCode'],
                    'zip': address['zip'],
                    'formatted': formatted,
                })
                addresses_set.add(str(formatted).lower())
        return data

    def get(self, *args, **kwargs):
        cursor = None
        results = []
        while True:
            query = self._get_addresses_query(cursor)
            response = requests.post(
                url=settings.SHOPIFY_URL,
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
