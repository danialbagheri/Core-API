from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import BlogPostSerializer


class BookmarkedBlogPostListAPIView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return self.request.user.bookmarked_blogposts.all()
