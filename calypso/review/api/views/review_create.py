from rest_framework import generics

from ..serializers import ReviewCreateSerializer


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['slug'] = self.kwargs.get('slug', None)
        return context
