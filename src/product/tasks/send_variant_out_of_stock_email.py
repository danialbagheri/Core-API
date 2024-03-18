from celery import current_app, Task

from product.models import ProductVariant
from product.services import VariantOutOfStockEmailService, MarketingVariantStockSubscriber


class SendVariantOutOfStockEmailTask(Task):
    name = 'products.tasks.SendVariantOutOfStockEmailTask'

    def run(self, variant_id: int):
        variant = ProductVariant.objects.get(id=variant_id)
        VariantOutOfStockEmailService(variant).send_email()
        MarketingVariantStockSubscriber(variant).subscribe_marketing_team()


current_app.register_task(SendVariantOutOfStockEmailTask())
