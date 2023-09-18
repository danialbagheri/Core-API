from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthAction
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView as DefaultOAuth2LoginView
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response


class OAuth2LoginView(DefaultOAuth2LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        provider = self.adapter.get_provider()
        app = provider.app
        client = self.get_client(request, app)
        action = request.GET.get('action', AuthAction.AUTHENTICATE)
        auth_url = self.adapter.authorize_url
        auth_params = provider.get_auth_params(request, action)

        pkce_params = provider.get_pkce_params()
        code_verifier = pkce_params.pop('code_verifier', None)
        auth_params.update(pkce_params)
        if code_verifier:
            request.session['pkce_code_verifier'] = code_verifier

        client.state = SocialLogin.stash_state(request)
        auth_params['redirect_uri'] = settings.SOCIAL_LOGIN_REDIRECT_URLS[app.provider]
        try:
            print(auth_url, auth_params)
            return HttpResponseRedirect(client.get_redirect_url(auth_url, auth_params))
        except OAuth2Error:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


google_oauth2_login = OAuth2LoginView.adapter_view(GoogleOAuth2Adapter)
facebook_oauth2_login = OAuth2LoginView.adapter_view(FacebookOAuth2Adapter)
