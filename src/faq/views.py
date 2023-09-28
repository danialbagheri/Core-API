from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import FAQFilter
from .models import Faq
from .serializers import FaqSerializer


class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FaqSerializer
    queryset = Faq.objects.filter(public=True)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FAQFilter
    lookup_field = 'pk'
