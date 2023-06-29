from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(DjoserUserViewSet):
    authentication_classes = (JWTAuthentication,)
