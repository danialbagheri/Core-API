from rest_framework import viewsets

from web.models import Configuration
from ..serializers import ConfigurationSerializer


class ConfigurationView(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    lookup_field = 'key'
