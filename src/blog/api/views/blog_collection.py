from rest_framework.viewsets import ReadOnlyModelViewSet

from blog.api.serializers import BlogCollectionSerializer
from blog.models import BlogCollection


class BlogCollectionViewSet(ReadOnlyModelViewSet):
    queryset = BlogCollection.objects.all()
    serializer_class = BlogCollectionSerializer
    lookup_field = 'slug'
