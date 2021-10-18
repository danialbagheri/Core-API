from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Tag
from .models import BlogPost, BlogCollection
from .serializers import BlogPostSerializer, BlogCollectionSerializer


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
    lookup_field = "slug"


class BookmarkedBlogPostAPIView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return self.request.user.bookmarked_blogposts.all()
