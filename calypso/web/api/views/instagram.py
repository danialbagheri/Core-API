from rest_framework.generics import ListAPIView

from web.api.serializers import InstagramSerializer
from web.models import InstagramPost


class InstagramListAPIView(ListAPIView):
    serializer_class = InstagramSerializer
    queryset = InstagramPost.objects.all()
