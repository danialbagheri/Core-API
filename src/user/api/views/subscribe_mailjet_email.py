from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.services import MailjetEmailManager


class SubscribeMailjetEmailAPIView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        if not email:
            return Response(
                data='Email is required',
                status=status.HTTP_400_BAD_REQUEST,
            )
        mailjet_email_manager = MailjetEmailManager(email)
        mailjet_email_manager.subscribe_email()
        return Response(
            data='Email subscribed',
            status=status.HTTP_200_OK,
        )
