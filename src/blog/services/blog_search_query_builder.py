from django.db.models import Q

from common.services import BaseService
from product.models import Tag, Keyword, Product


class BlogSearchQueryBuilder(BaseService):
    service_name = 'Blog Search Query Builder'

    def __init__(self, search_input):
        super().__init__(search_input=search_input)
        self.input_parts = search_input.split(' ')

    def _build_blog_title_query(self):
        query = Q()
        for input_part in self.input_parts:
            query |= Q(title__icontains=input_part)
        return query

    def _get_search_related_product_ids(self):
        query = Q()
        for input_part in self.input_parts:
            tag = Tag.objects.filter(Q(name__icontains=input_part)).first()
            keyword = Keyword.objects.filter(Q(name__icontains=input_part)).first()
            query_part = (
                Q(name__icontains=input_part) |
                Q(sub_title__icontains=input_part) |
                Q(variants__sku__icontains=input_part)
            )
            if tag is not None:
                query_part |= Q(tags=tag)
            if keyword is not None:
                query_part |= Q(keyword=keyword)
            query |= query_part
        return list(Product.objects.filter(query).values_list('id', flat=True).distinct())

    def _build_blog_products_query(self):
        search_product_ids = self._get_search_related_product_ids()
        return Q(related_products__id__in=search_product_ids)

    def build_query(self):
        return Q(
            self._build_blog_title_query() |
            self._build_blog_products_query(),
            published=True,
        )
