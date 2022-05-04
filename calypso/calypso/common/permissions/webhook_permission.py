import base64
import hashlib
import hmac

from django.conf import settings
from rest_framework.permissions import BasePermission


class WebhookPermission(BasePermission):
    def has_permission(self, request, view):
        data = request.body
        hmac_token = request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256')
        if not hmac_token:
            return False

        digest = hmac.new(
            settings.SHOPIFY_SHARED_SECRET_KEY.encode('utf-8'),
            data,
            digestmod=hashlib.sha256,
        ).digest()
        computed_hmac = base64.b64encode(digest)
        return hmac.compare_digest(computed_hmac, hmac_token.encode('utf-8'))
