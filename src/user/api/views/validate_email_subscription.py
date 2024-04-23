from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.services import EmailSubscriptionValidator


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
        email_subscription_validator = EmailSubscriptionValidator(email)
        is_subscribed = email_subscription_validator.validate()
        return Response(
            data={'is_subscribed': is_subscribed},
            status=status.HTTP_200_OK,
        )
