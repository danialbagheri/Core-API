from django.db.models import Q

from common.services import BaseService


class MenuSearchQueryBuilder(BaseService):
    service_name = 'Menu Search Query Builder'

    def __init__(self, search_input):
        super().__init__(search_input=search_input)
        self.input_parts = search_input.split(' ')

    def build_query(self):
        query = Q()
        for input_part in self.input_parts:
            query |= Q(text__icontains=input_part)
        return query
