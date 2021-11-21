from rest_framework import viewsets

from web.models import Slider
from ..serializers import SliderSerializer


class SliderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.query_params.get('slug', False)
        if slug:
            queryset = queryset.filter(slug=slug)
        return queryset
