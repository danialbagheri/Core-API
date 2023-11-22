from rest_framework.generics import RetrieveAPIView

from web.models import Menu
from ..serializers import MenuSerializer


class MenuRetrieveAPIView(RetrieveAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.filter(is_active=True)
    lookup_field = 'slug'
