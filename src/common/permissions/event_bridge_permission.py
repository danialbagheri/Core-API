from django.conf import settings
from rest_framework.permissions import BasePermission


class EventBridgePermission(BasePermission):
    def has_permission(self, request, view):
        amazon_eventbridge_secret = request.headers.get('linco-eventbridge-secret')
        return amazon_eventbridge_secret and amazon_eventbridge_secret == settings.AMAZON_EVENTBRIDGE_SECRET
