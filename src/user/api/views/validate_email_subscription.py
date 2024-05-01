from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.services import MailjetEmailManager


class ValidateEmailSubscriptionAPIView(APIView):
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
        is_subscribed = mailjet_email_manager.validate()
        return Response(
            data={'is_subscribed': is_subscribed, status: mailjet_email_manager.mailjet_email_status.value},
            status=status.HTTP_200_OK,
        )
