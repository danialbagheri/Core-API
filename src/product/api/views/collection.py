from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Collection
from ..serializers import CollectionSerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = 'slug'
