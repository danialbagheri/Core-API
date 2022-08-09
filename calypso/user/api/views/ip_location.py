from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.services import IPLocationFinderService


class IPLocationAPIView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ('get',)

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs):
        ip = kwargs.get('ip', None)
        ip_location_finder = IPLocationFinderService(ip)
        ip_location_finder.receive_location_data()

        if not ip_location_finder.country:
            return Response(
                data='Invalid IP',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data={'country': ip_location_finder.country},
            status=status.HTTP_200_OK,
        )
