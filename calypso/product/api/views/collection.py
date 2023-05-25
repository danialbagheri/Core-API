from rest_framework import viewsets

from product.models import Collection
from ..serializers import CollectionSerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = 'slug'
