from rest_framework.viewsets import ReadOnlyModelViewSet

from bundles.models import Bundle
from ..serializers import BundleListSerializer, BundleRetrieveSerializer


class BundleReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Bundle.objects.filter(is_active=True)
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return BundleListSerializer
        return BundleRetrieveSerializer
