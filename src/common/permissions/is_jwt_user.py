from allauth.socialaccount.models import SocialAccount, SocialToken
from django.utils import timezone
from rest_framework.permissions import BasePermission

from oauth2.services import GoogleTokenRefresher, TokenRefreshFailed


class IsJWTUser(BasePermission):
    message = 'Social token has expired.'

    def has_permission(self, request, view):
        social_account = SocialAccount.objects.filter(user=request.user).first()
        if not social_account:
            return True

        token = SocialToken.objects.get(account=social_account)
        token_expired = token.expires_at > timezone.now()
        if not token_expired:
            return True
        if not token.token_secret:
            return False

        try:
            GoogleTokenRefresher(token).refresh_token()
        except TokenRefreshFailed:
            return False
        return True
