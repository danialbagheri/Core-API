from django.shortcuts import render
from .models import Page
from rest_framework import viewsets
from .serializers import PageSerializer
# Create your views here.
class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.filter(published=True)
    serializer_class = PageSerializer
    lookup_field = 'slug'