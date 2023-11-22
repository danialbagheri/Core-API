from django.db import transaction
from django.db.models import Q
from rest_framework import generics

from product.api.serializers import ProductSerializer
from product.models import Product, Tag, Keyword
from web.models import SearchQuery


class Search(generics.ListAPIView):
    serializer_class = ProductSerializer

    @staticmethod
    def _update_search_query(query):
        with transaction.atomic():
            search_query, _ = SearchQuery.objects.get_or_create(text=query.lower())
            search_query.count += 1
            search_query.save()

    @staticmethod
    def _affect_query(query):
        tag = Tag.objects.filter(Q(name__icontains=query)).first()
        keyword = Keyword.objects.filter(Q(name__icontains=query)).first()
        query = (
            Q(name__icontains=query) |
            Q(sub_title__icontains=query) |
            Q(variants__sku__icontains=query) |
            Q(variants__name__icontains=query)
        )
        if tag is not None:
            query |= Q(tags=tag)
        if keyword is not None:
            query |= Q(keyword=keyword)
        return query

    def _get_phrase_search_results(self, search_input):
        query = self._affect_query(search_input)
        return list(Product.objects.filter(query, is_public=True))

    def get_queryset(self):
        is_valid_query = False
        queryset = Product.objects.filter(is_public=True)
        search_input = self.request.query_params.get('q', '')
        phrase_search_products = self._get_phrase_search_results(search_input)
        input_parts = search_input.split(' ')
        query = Q()
        for input_part in input_parts:
            if input_part is not None and len(input_part) >= 2:
                is_valid_query = True
                self._update_search_query(input_part)
                query |= self._affect_query(input_part)
        if not is_valid_query:
            return []

        word_search_products = list(queryset.filter(query).distinct())
        products = phrase_search_products + word_search_products
        return list(dict.fromkeys(products))
