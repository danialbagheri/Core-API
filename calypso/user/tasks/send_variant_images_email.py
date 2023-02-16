from celery import Task, current_app

from user.services import VariantImageZipper, VariantRequestEmailService


class SendVariantImagesEmailTask(Task):
    name = 'users.tasks.SendVariantImagesEmailTask'

    def run(self, sku_list, email, image_format):
        images_zipper = VariantImageZipper(sku_list, image_format)
        zip_buffer = images_zipper.create_zip_file()
        images_email_service = VariantRequestEmailService(sku_list, email, zip_buffer)
        images_email_service.send_email()


current_app.register_task(SendVariantImagesEmailTask())
