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
    def _affect_query(queryset, query):
        tag = Tag.objects.filter(Q(name__icontains=query)).first()
        keyword = Keyword.objects.filter(Q(name__icontains=query)).first()
        if tag is not None:
            return queryset.filter(Q(tags=tag))
        elif keyword is not None:
            return queryset.filter(Q(keyword=keyword))
        return queryset.filter(
            Q(name__icontains=query) |
            Q(sub_title__icontains=query) |
            Q(variants__sku__icontains=query)
        )

    def get_queryset(self):
        is_valid_query = False
        queryset = Product.objects.all()
        full_query = self.request.query_params.get('q', '')
        query_parts = full_query.split(' ')
        for query in query_parts:
            if query is not None and len(query) >= 2:
                is_valid_query = True
                self._update_search_query(query)
                self._affect_query(queryset, query)
        if not is_valid_query:
            return []
        return queryset.distinct()
