from rest_framework.generics import RetrieveAPIView

from ..serializers import IconGroupSerializer
from ...models import IconGroup


class IconGroupRetrieveAPIView(RetrieveAPIView):
    serializer_class = IconGroupSerializer
    lookup_field = 'slug'
    queryset = IconGroup.objects.filter(is_active=True)
