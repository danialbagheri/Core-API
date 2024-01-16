from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from blog.models import BlogPost
from product.models import Tag
from ..serializers import BlogPostSerializer


class BlogPostViewSet(ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = BlogPost.objects.filter(published=True)
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

