from django.shortcuts import render
from .models import BlogPost, BlogCollection
from django.db.models import Q
from .serializers import BlogPostSerializer, BlogCollectionSerializer
from rest_framework import viewsets
from product.models import Tag
# Create your views here.
class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogPostSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        tag_q = self.request.query_params.get('tag', None)
        count = self.request.query_params.get('count', None)
        if tag_q:
            try:
                tag_instance = Tag.objects.get(Q(slug__icontains=tag_q))
                queryset = queryset.filter(tags=tag_instance)
            except:
                pass
        if count:
            queryset = queryset[: int(count)]
        return queryset



class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCollection.objects.all()
    serializer_class = BlogCollectionSerializer
    lookup_field="slug"