from product.models import ProductVariant
from user.models import ReviewReminder, ReviewReminderBoughtVariant


class ReviewReminderUndoService:
    def __init__(self, refund_data):
        self._refund_data = refund_data

    def _update_review_reminder_bought_variants(self, review_reminder):
        variants_map = {
            variant.shopify_rest_variant_id: variant.id for variant in ProductVariant.objects.filter(is_public=True)
        }
        refund_line_items = self._refund_data['refund_line_items']
        for refund_line_item in refund_line_items:
            restock_type = refund_line_item['restock_type']
            if restock_type not in ['cancel', 'return']:
                continue
            line_item = refund_line_item['line_item']
            shopify_variant_id = line_item['variant_id']
            variant_id = variants_map.get(shopify_variant_id)
            if not variant_id:
                continue
            quantity = refund_line_item['quantity']
            bought_variant = ReviewReminderBoughtVariant.objects.get(
                review_reminder=review_reminder,
                variant_id=variant_id,
            )
            if bought_variant.quantity > quantity:
                bought_variant.quantity -= quantity
                bought_variant.save()
            else:
                review_reminder.bought_variants.remove(bought_variant.variant)
                bought_variant.delete()

    def undo_review_reminder(self):
        order_id = self._refund_data['order_id']
        review_reminder = ReviewReminder.objects.filter(order_id=order_id).first()
        if not review_reminder:
            return

        self._update_review_reminder_bought_variants(review_reminder)
