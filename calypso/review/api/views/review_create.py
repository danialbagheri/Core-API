from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import ReviewCreateSerializer


class CreateReview(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = ReviewCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['slug'] = self.kwargs.get('slug', None)
        return context
