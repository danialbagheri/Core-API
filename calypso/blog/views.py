from django.shortcuts import render
from .models import BlogPost
from django.db.models import Q
from .serializers import BlogPostSerializer
from rest_framework import viewsets
from product.models import Tag
# Create your views here.
class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogPostSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        tag_q = self.request.query_params.get('tag', None)
        if tag_q:
            try:
                # import pdb
                # pdb.set_trace()
                tag_instance = Tag.objects.get(Q(slug__icontains=tag_q))
                queryset = queryset.filter(tags=tag_instance)
            except:
                pass
        return queryset