from celery import current_app, Task

from product.models import ProductVariant
from product.services import VariantOutOfStockEmailService


class SendVariantOutOfStockEmailTask(Task):
    name = 'products.tasks.SendVariantOutOfStockEmailTask'

    def run(self, variant_id: int):
        variant = ProductVariant.objects.get(id=variant_id)
        VariantOutOfStockEmailService(variant).send_email()


current_app.register_task(SendVariantOutOfStockEmailTask())
