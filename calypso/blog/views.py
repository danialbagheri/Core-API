from django.shortcuts import render
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework import viewsets
# Create your views here.
class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "slug"