from rest_framework.generics import CreateAPIView

from review.api.serializers import ReviewImageSerializer


class ReviewImageAPIView(CreateAPIView):
    serializer_class = ReviewImageSerializer
