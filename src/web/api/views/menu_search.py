from rest_framework.generics import ListAPIView

from web.api.serializers import MenuSerializer
from web.models import Menu
from web.services import MenuSearchQueryBuilder


class MenuSearchListAPIView(ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        search_input = self.request.query_params.get('q', '')
        search_query = MenuSearchQueryBuilder(search_input).build_query()
        return Menu.objects.filter(
            search_query,
            is_active=True,
        )
