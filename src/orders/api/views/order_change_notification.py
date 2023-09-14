from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import EventBridgePermission
from orders.tasks import OrderChangeNotificationTask


class OrderChangeNotificationAPI(APIView):
    permission_classes = (EventBridgePermission,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        OrderChangeNotificationTask().delay(request.data)
        return Response(data={}, status=status.HTTP_200_OK)
