from datetime import datetime, timedelta

from common.services import BaseService
from product.models import ProductVariant
from user.models import AbandonedCheckout, SentEmail, CheckoutItem
from user.resources import AbandonedCheckoutResource


class AbandonedCheckoutRetriever(BaseService):
    service_name = 'Abandoned Checkout Retriever'

    @staticmethod
    def _get_checkouts_data():
        yesterday = datetime.now() - timedelta(days=1)
        two_days_ago = datetime.now() - timedelta(days=2)
        abandoned_checkout_resource = AbandonedCheckoutResource()
        checkouts_data = abandoned_checkout_resource.get_abandoned_checkouts(
            status='open',
            updated_at_min=two_days_ago,
            updated_at_max=yesterday,
        )
        while True:
            next_page_url = abandoned_checkout_resource.next_page_url
            if not next_page_url:
                break

            checkouts_data += abandoned_checkout_resource.get_abandoned_checkouts(url=next_page_url)
        return checkouts_data

    @staticmethod
    def _create_checkout_items(checkout, line_items_data):
        checkout_items_to_create = []
        for line_item_data in line_items_data:
            variant = ProductVariant.objects.get(shopify_rest_variant_id=line_item_data['variant_id'])
            checkout_items_to_create.append(CheckoutItem(
                checkout=checkout,
                variant=variant,
                quantity=line_item_data['quantity'],
                price=float(line_item_data['price']),
            ))
        CheckoutItem.objects.bulk_create(checkout_items_to_create)

    def _create_checkout(self, checkout_data):
        checkout_id = checkout_data['id']
        email = checkout_data['email']
        if (
            AbandonedCheckout.objects.filter(legacy_id=checkout_id).exists() or
            SentEmail.objects.filter(
                template_name=SentEmail.TEMPLATE_ABANDONED_CHECKOUT,
                email=email,
                sent_date__gte=datetime.now() - timedelta(days=30),
            ).exists()
        ):
            return

        customer_data = checkout_data['customer'] or {}
        checkout = AbandonedCheckout.objects.create(
            legacy_id=checkout_id,
            created_at=checkout_data['created_at'],
            abandoned_checkout_url=checkout_data['abandoned_checkout_url'],
            cart_token=checkout_data['cart_token'],
            email=email,
            customer_id=customer_data.get('id'),
            customer_first_name=customer_data.get('first_name'),
            customer_last_name=customer_data.get('last_name'),
        )
        self._create_checkout_items(checkout, checkout_data['line_items'])

    def get_checkouts(self):
        checkouts_data = self._get_checkouts_data()
        checkouts = []
        for checkout_data in checkouts_data:
            checkouts.append(self._create_checkout(checkout_data))
        return checkouts
