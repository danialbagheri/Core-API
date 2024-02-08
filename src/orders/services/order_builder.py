from common.services import BaseService
from orders.models import Order, OrderItem


class OrderBuilder(BaseService):
    def __init__(self, order_data):
        super().__init__(order_data=order_data)
        self.order_data = order_data

    def _build_order(self):
        return Order.objects.create(
            created_at=self.order_data['created_at'],
            updated_at=self.order_data['updated_at'],
            shopify_graphql_id=self.order_data['admin_graphql_api_id'],
            order_name=self.order_data['name'],
            financial_status=self.order_data['financial_status'],
            subtotal_price=self.order_data['subtotal_price'],
            total_discounts=self.order_data['total_discounts'],
            total_line_items_price=self.order_data['total_line_items_price'],
            total_price=self.order_data['total_price'],
        )

    def _build_order_items(self, order: Order):
        line_items_data = self.order_data['line_items']
        order_items_to_create = []
        for line_item_data in line_items_data:
            order_items_to_create.append(OrderItem(
                order=order,
                shopify_graphql_id=line_item_data['admin_graphql_api_id'],
                product_id=line_item_data['product_id'],
                name=line_item_data['name'],
                variant_id=line_item_data['variant_id'],
                sku=line_item_data['sku'],
                price=line_item_data['price'],
                total_discount=line_item_data['total_discount'],
                quantity=line_item_data['quantity'],
            ))
        OrderItem.objects.bulk_create(order_items_to_create)

    def build(self):
        order = self._build_order()
        self._build_order_items(order)
