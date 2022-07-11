from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import PushSubscriberSerializer


class PushSubscriberCreateAPIView(CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = PushSubscriberSerializer
