from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import WebhookPermission
from user.tasks import OrderPaidWebhookTask


class OrderPaidWebhookAPI(APIView):
    permission_classes = (WebhookPermission,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        OrderPaidWebhookTask().delay(request.data)
        return Response(data={}, status=status.HTTP_200_OK)
