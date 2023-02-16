import ast

from celery import Task, current_app

from user.models import VariantImageRequest
from user.services import VariantImageZipper, VariantRequestEmailService


class SendVariantImagesEmailTask(Task):
    name = 'users.tasks.SendVariantImagesEmailTask'

    def run(self, variant_image_request_id):
        variant_image_request = VariantImageRequest.objects.get(id=variant_image_request_id)
        sku_list = ast.literal_eval(variant_image_request.sku_list)
        images_zipper = VariantImageZipper(sku_list, variant_image_request.image_format)
        zip_buffer = images_zipper.create_zip_file()
        images_email_service = VariantRequestEmailService(variant_image_request, zip_buffer)
        images_email_service.send_email()


current_app.register_task(SendVariantImagesEmailTask())
