from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from web.models import TopBar
from web.serializers import TopBarSerializer


class TopBarListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TopBarSerializer
    queryset = TopBar.objects.filter(is_active=True).all()
