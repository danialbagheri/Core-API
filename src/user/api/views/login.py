import uuid
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import SessionCookie


class LoginAPIView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        keep_logged_in = request.query_params.get('keep_logged_in')
        keep_logged_in = keep_logged_in != 'False'
        if keep_logged_in:
            session_cookie = uuid.uuid4()
            expire_date = timezone.now() + timedelta(days=30)
            SessionCookie.objects.create(user=serializer.user, cookie=session_cookie, expire_date=expire_date)
            response.set_cookie('login_token', session_cookie, expire_date)
        return response
