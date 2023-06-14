from django.db.models import Count

from product.models import Product


class RelatedProductsRetriever:
    def __init__(self, product: Product):
        self.product = product

    def get_related_products(self, related_products_count):
        tag_ids = self.product.tags.values_list('id', flat=True)
        related_products = Product.objects.filter(
            tags__id__in=tag_ids,
            is_public=True,
        ).exclude(
            id=self.product.id
        ).annotate(
            num_common_tags=Count('pk'),
        ).order_by('-num_common_tags')[:related_products_count]
        return related_products
