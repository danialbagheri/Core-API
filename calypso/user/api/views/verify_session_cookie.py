from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import SessionCookie


class VerifySessionCookieAPIView(GenericAPIView):
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        cookie = request.COOKIES.get('login_token', None)
        session_cookie = SessionCookie.objects.filter(cookie=cookie).first()
        if not session_cookie:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if timezone.now() > session_cookie.expire_date:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = session_cookie.user
        refresh_token = RefreshToken.for_user(user)
        return Response(
            data={'refresh': str(refresh_token), 'access': str(refresh_token.access_token)},
            status=status.HTTP_201_CREATED,
        )
