from collections import defaultdict

from django.utils import timezone

from common.services import BaseService
from orders.models import Order
from product.models import Product, ProductVariant


class OrdersMetricsAnalyzer(BaseService):
    service_name = 'Orders Metrics Analyzer'

    def __init__(self):
        self.now = timezone.now()
        super().__init__(now=self.now)
        self.total_number_of_orders = 0
        self.weekday_orders = defaultdict(int)
        self.products_count = defaultdict(int)
        self.variants_count = defaultdict(int)

    def analyze_metrics(self):
        orders = Order.objects.filter(created_at__gte=self.now - timezone.timedelta(days=7))
        for order in orders:
            self.total_number_of_orders += 1
            self.weekday_orders[order.created_at.weekday()] += 1
            for item in order.items.all():
                if item.product_id:
                    self.products_count[item.product_id] += 1
                if item.variant_id:
                    self.variants_count[item.variant_id] += 1

    def get_peak_orders_day(self):
        if not self.weekday_orders:
            return '-'
        weekday_number = max(self.weekday_orders, key=self.weekday_orders.get)
        return {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday',
        }[weekday_number]

    def get_most_popular_ordered_product(self):
        if not self.products_count:
            return '-'
        product_id = max(self.products_count, key=self.products_count.get)
        product = Product.objects.get(legacy_id=product_id)
        return product.name

    def get_most_popular_ordered_variant(self):
        if not self.variants_count:
            return '-'
        variant_id = max(self.variants_count, key=self.variants_count.get)
        variant = ProductVariant.objects.get(shopify_rest_variant_id=variant_id)
        return f'{variant.product.name} - {variant.name}'
