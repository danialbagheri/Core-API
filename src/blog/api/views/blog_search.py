from rest_framework.generics import ListAPIView

from blog.api.serializers import BlogPostSerializer
from blog.models import BlogPost
from blog.services import BlogSearchQueryBuilder


class BlogSearchListAPIView(ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        search_input = self.request.query_params.get('q', '')
        query = BlogSearchQueryBuilder(search_input).build_query()
        return BlogPost.objects.filter(query)
