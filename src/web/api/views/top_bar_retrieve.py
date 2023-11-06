from rest_framework.generics import RetrieveAPIView

from web.api.serializers import TopBarSerializer
from web.models import TopBar


class TopBarRetrieveAPIView(RetrieveAPIView):
    serializer_class = TopBarSerializer
    queryset = TopBar.objects.filter(is_active=True)
    lookup_field = 'slug'
