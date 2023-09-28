import django_filters

from faq.models import Faq


class FAQFilter(django_filters.FilterSet):
    slug = django_filters.CharFilter(field_name='product__slug')

    class Meta:
        model = Faq
        fields = {
            'category': ['exact'],
        }
