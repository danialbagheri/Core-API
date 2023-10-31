from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import WebhookPermission
from product.tasks import ProductEditTask


class ProductEditWebhookAPI(APIView):
    permission_classes = (WebhookPermission,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        vendor = request.data.get('vendor', None)
        if vendor and vendor != settings.BRAND_NAME:
            return Response(data={}, status=status.HTTP_200_OK)
        graphql_id = request.data.get('admin_graphql_api_id', None)
        ProductEditTask().delay(graphql_id)
        return Response(data={}, status=status.HTTP_200_OK)
