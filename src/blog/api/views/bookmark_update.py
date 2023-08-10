from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from blog.models import BlogPost


class BookmarkUpdateAPIView(UpdateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BlogPost.objects.all()
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        blog_post = self.get_object()
        user = request.user
        action = self.request.data.get('action', 'add')
        if action == 'add':
            user.bookmarked_blogposts.add(blog_post)
        elif action == 'remove':
            user.bookmarked_blogposts.remove(blog_post)
        else:
            return Response(
                data='Invalid action.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data='Action done successfully',
            status=status.HTTP_200_OK,
        )
