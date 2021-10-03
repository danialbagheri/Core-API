import uuid

from rest_framework import generics

from ..serializers import ReviewRateSerializer
from ...models import Review


class RateReview(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewRateSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cookie = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cookie'] = self._cookie
        return context

    def patch(self, request, *args, **kwargs):
        self._cookie = request.COOKIES.get('calypsosun_token', None)
        if not self._cookie:
            self._cookie = uuid.uuid4()
            response = super().patch(request, *args, **kwargs)
            response.set_cookie('calypsosun_token', self._cookie)
            return response
        return super().patch(request, *args, **kwargs)
