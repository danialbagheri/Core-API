from django.shortcuts import render
from rest_framework import viewsets
from .models import Faq
from .serializers import FaqSerializer
# Create your views here.

class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faq.objects.filter(public=True)
    serializer_class = FaqSerializer
