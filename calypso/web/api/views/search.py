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

    def get_queryset(self):
        queryset = []
        query = self.request.query_params.get('q', None)
        if query is not None and len(query) >= 2:
            self._update_search_query(query)
            try:
                tag = Tag.objects.filter(Q(name__icontains=query)).first()
                keyword = Keyword.objects.filter(Q(name__icontains=query)).first()
                if tag is not None:
                    queryset = Product.objects.filter(Q(tags=tag)).distinct()
                elif keyword is not None:
                    queryset = Product.objects.filter(Q(keyword=keyword)).distinct()
                else:
                    queryset = Product.objects.filter(
                        Q(name__icontains=query) |
                        Q(sub_title__icontains=query) |
                        Q(variants__sku__icontains=query)
                    ).distinct()
            except:
                pass
        return queryset
