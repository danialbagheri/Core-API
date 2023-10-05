from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.tasks import SendWelcomeDiscountEmailTask


class WelcomeDiscountEmailAPIView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        if not email:
            return Response(data='Email not sent.', status=status.HTTP_400_BAD_REQUEST)
        SendWelcomeDiscountEmailTask().delay(email)
