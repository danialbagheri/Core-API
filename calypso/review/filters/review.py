import django_filters

from review.models import Review


class ReviewFilter(django_filters.FilterSet):
    product_slug = django_filters.CharFilter(field_name='product__slug')

    class Meta:
        model = Review
        fields = {}
