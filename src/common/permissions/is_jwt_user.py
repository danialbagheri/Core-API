from allauth.socialaccount.models import SocialAccount, SocialToken
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


class IsJWTUser(IsAuthenticated):
    def has_permission(self, request, view):
        social_account = SocialAccount.objects.filter(user=request.user).first()
        if not social_account:
            return True

        token = SocialToken.objects.get(account=social_account)
        return token.expires_at > timezone.now()
