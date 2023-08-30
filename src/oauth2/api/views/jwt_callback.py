from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthError, ProviderException
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from allauth.utils import get_request_param
from django.core.exceptions import PermissionDenied
from requests import RequestException
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class JWTOAuth2CallbackView(OAuth2CallbackView):
    def handle_errors(self, request):
        if 'error' not in request.GET and 'code' in request.GET:
            return None

        # Distinguish cancel from error
        auth_error = request.GET.get('error', None)
        if auth_error == self.adapter.login_cancelled_error:
            error = AuthError.CANCELLED
        else:
            error = AuthError.UNKNOWN
        return Response(data={'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def create_social_login(self, request, app, client):
        access_token = self.adapter.get_access_token_data(request, app, client)
        token = self.adapter.parse_token(access_token)
        token.app = app
        social_login = self.adapter.complete_login(
            request, app, token, response=access_token
        )
        social_login.token = token
        if self.adapter.supports_state:
            social_login.state = SocialLogin.verify_and_unstash_state(
                request, get_request_param(request, 'state')
            )
        else:
            social_login.state = SocialLogin.unstash_state(request)

        social_login.lookup()
        if not social_login.is_existing:
            get_adapter(request).save_user(request, social_login)

        return social_login

    def dispatch(self, request, *args, **kwargs):
        if request.method != 'GET':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        error_response = self.handle_errors(request)
        if error_response:
            return error_response

        app = self.adapter.get_provider().app
        client = self.get_client(self.request, app)

        try:
            social_login = self.create_social_login(request, app, client)
        except (
            PermissionDenied,
            OAuth2Error,
            RequestException,
            ProviderException,
        ):
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

        user = social_login.user
        refresh_token = RefreshToken.for_user(user)
        return Response(data={
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        })


google_oauth2_callback = JWTOAuth2CallbackView.adapter_view(GoogleOAuth2Adapter)
facebook_oauth2_callback = JWTOAuth2CallbackView.adapter_view(FacebookOAuth2Adapter)
