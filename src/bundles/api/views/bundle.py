from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from bundles.models import Bundle
from ..filters import BundleFilter
from ..serializers import BundleListSerializer, BundleRetrieveSerializer


class BundleReadOnlyViewSet(ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BundleFilter
    queryset = Bundle.objects.filter(is_active=True)
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return BundleListSerializer
        return BundleRetrieveSerializer
