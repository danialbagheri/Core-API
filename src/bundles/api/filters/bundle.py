import django_filters

from bundles.models import Bundle


class BundleFilter(django_filters.FilterSet):
    product_id = django_filters.NumberFilter(field_name='items__product_id')

    class Meta:
        model = Bundle
        fields = {}
