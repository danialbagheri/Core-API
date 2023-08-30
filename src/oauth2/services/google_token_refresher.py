from datetime import timedelta

import requests
from allauth.socialaccount.models import SocialToken, SocialApp
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.utils import timezone

from common.services import BaseService


class TokenRefreshFailed(Exception):
    pass


class GoogleTokenRefresher(BaseService):
    service_name = 'Google Token Refresher'
    GRANT_TYPE = 'refresh_token'

    def __init__(self, token: SocialToken):
        super().__init__(user=token.account.user)
        self.token = token

    def refresh_token(self):
        app = SocialApp.objects.get(provider='google')
        url = GoogleOAuth2Adapter.access_token_url
        data = {
            'refresh_token': self.token.token_secret,
            'client_id': app.client_id,
            'client_secret': app.secret,
            'grant_type': self.GRANT_TYPE,
        }
        response = requests.post(
            url=url,
            data=data,
        )
        if not response.ok:
            raise TokenRefreshFailed
        new_token_data = response.json()
        self.token.token = new_token_data['access_token']
        expires_in = new_token_data['expires_in']
        self.token.expires_at = timezone.now() + timedelta(seconds=int(expires_in))
        self.token.save()
