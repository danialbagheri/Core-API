import logging

from celery import Task, current_app

from product.services import ProductEditor

logger = logging.getLogger(__name__)


class ProductEditTask(Task):
    name = 'ProductEdit'

    def run(self, product_id):
        product_editor = ProductEditor(product_id)
        product_editor.edit_product()


current_app.register_task(ProductEditTask())
