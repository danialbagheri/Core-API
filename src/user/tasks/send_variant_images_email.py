import ast

from celery import Task, current_app

from user.models import VariantImageRequest
from user.services import VariantImageZipper, VariantRequestEmailService, VariantImagesRetriever


class SendVariantImagesEmailTask(Task):
    name = 'users.tasks.SendVariantImagesEmailTask'

    def run(self, variant_image_request_id):
        variant_image_request = VariantImageRequest.objects.get(id=variant_image_request_id)
        variant_images_retriever = VariantImagesRetriever(variant_image_request)
        variant_images_retriever.retrieve_variant_image()
        image_formats = ast.literal_eval(variant_image_request.image_formats)
        images_zipper = VariantImageZipper(variant_images_retriever.variant_images, image_formats)
        zip_buffer = images_zipper.create_zip_file()
        images_email_service = VariantRequestEmailService(variant_image_request, zip_buffer)
        images_email_service.send_email(variant_images_retriever.sku_list_without_image)


current_app.register_task(SendVariantImagesEmailTask())
